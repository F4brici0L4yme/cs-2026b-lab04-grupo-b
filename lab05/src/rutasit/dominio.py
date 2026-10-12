"""Entidades, valores y reglas centrales del dominio RutaSIT."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import uuid4

from .compartido import Id

RADIO_TIERRA_M = 6_371_000.0


class EstadoBus(Enum):
    EN_ESPERA = "EN_ESPERA"
    EN_RUTA = "EN_RUTA"
    EN_PARADERO = "EN_PARADERO"
    DESVIADO = "DESVIADO"
    FUERA_DE_SERVICIO = "FUERA_DE_SERVICIO"


@dataclass(frozen=True, slots=True)
class UbicacionGPS:
    latitud: float
    longitud: float
    capturada_en: datetime

    def __post_init__(self) -> None:
        if not -90.0 <= self.latitud <= 90.0:
            raise ValueError("La latitud debe estar entre -90 y 90 grados")
        if not -180.0 <= self.longitud <= 180.0:
            raise ValueError("La longitud debe estar entre -180 y 180 grados")
        if self.capturada_en.tzinfo is None or self.capturada_en.utcoffset() is None:
            raise ValueError("capturada_en debe incluir zona horaria")

    def distancia_a(self, otra: UbicacionGPS) -> float:
        """Distancia haversine aproximada, en metros."""
        lat1, lon1, lat2, lon2 = map(
            math.radians,
            (self.latitud, self.longitud, otra.latitud, otra.longitud),
        )
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        a = min(1.0, max(0.0, a))
        return 2 * RADIO_TIERRA_M * math.asin(math.sqrt(a))

    def es_reciente(self, ahora: datetime, antiguedad_max: timedelta) -> bool:
        if ahora.tzinfo is None or ahora.utcoffset() is None:
            raise ValueError("ahora debe incluir zona horaria")
        if antiguedad_max < timedelta(0):
            raise ValueError("antiguedad_max no puede ser negativa")
        edad = ahora - self.capturada_en
        return timedelta(0) <= edad <= antiguedad_max


@dataclass(frozen=True, slots=True)
class Paradero:
    id: Id
    nombre: str
    ubicacion: UbicacionGPS

    def __post_init__(self) -> None:
        if not str(self.id).strip() or not self.nombre.strip():
            raise ValueError("El paradero requiere identificador y nombre")

    def distancia_a(self, ubicacion: UbicacionGPS) -> float:
        return self.ubicacion.distancia_a(ubicacion)


@dataclass(frozen=True, slots=True)
class Ruta:
    id: Id
    nombre: str
    paraderos: tuple[Paradero, ...]
    puntos_trazado: tuple[UbicacionGPS, ...]

    def __post_init__(self) -> None:
        if not str(self.id).strip() or not self.nombre.strip():
            raise ValueError("La ruta requiere identificador y nombre")
        if not self.paraderos:
            raise ValueError("La ruta debe contener al menos un paradero")
        if len(self.puntos_trazado) < 2:
            raise ValueError("El trazado requiere al menos dos puntos")

    def esta_en_ruta(self, ubicacion: UbicacionGPS, tolerancia_m: float) -> bool:
        """Comprueba proximidad a puntos muestreados del trazado.

        Calcula distancia a segmentos en una proyección local equirectangular.
        Para producción se debe validar la geometría oficial del SIT.
        """
        if tolerancia_m < 0:
            raise ValueError("tolerancia_m no puede ser negativa")
        latitud_referencia = math.radians(ubicacion.latitud)

        def proyectar(punto: UbicacionGPS) -> tuple[float, float]:
            x = RADIO_TIERRA_M * math.radians(punto.longitud) * math.cos(latitud_referencia)
            y = RADIO_TIERRA_M * math.radians(punto.latitud)
            return x, y

        px, py = proyectar(ubicacion)
        puntos = [proyectar(punto) for punto in self.puntos_trazado]
        distancias: list[float] = []
        for (ax, ay), (bx, by) in zip(puntos, puntos[1:]):
            dx, dy = bx - ax, by - ay
            longitud2 = dx * dx + dy * dy
            if longitud2 == 0:
                distancias.append(math.hypot(px - ax, py - ay))
                continue
            t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / longitud2))
            distancias.append(math.hypot(px - (ax + t * dx), py - (ay + t * dy)))
        return min(distancias) <= tolerancia_m

    def paradero_por_id(self, paradero_id: Id) -> Paradero | None:
        return next((p for p in self.paraderos if p.id == paradero_id), None)

    def siguiente_paradero(self, ubicacion: UbicacionGPS) -> Paradero | None:
        """Devuelve el paradero más cercano como aproximación del siguiente."""
        return min(self.paraderos, key=lambda p: p.distancia_a(ubicacion), default=None)


@dataclass(slots=True)
class UsuarioSistema:
    """Identidad seudónima para cuentas operativas, sin PII de perfil."""

    id_anonimo: Id
    activo: bool = True

    def desactivar(self) -> None:
        self.activo = False


@dataclass(slots=True)
class Conductor(UsuarioSistema):
    def puede_conducir(self) -> bool:
        return self.activo


@dataclass(slots=True)
class Bus:
    id: Id
    ruta_id: Id | None = None
    conductor_id: Id | None = None
    estado: EstadoBus = EstadoBus.EN_ESPERA
    ultima_ubicacion: UbicacionGPS | None = None
    historial: list[UbicacionGPS] = field(default_factory=list)

    def actualizar_ubicacion(self, ubicacion: UbicacionGPS) -> None:
        if self.estado is EstadoBus.FUERA_DE_SERVICIO:
            raise ValueError("No se actualiza telemetría de un bus fuera de servicio")
        self.ultima_ubicacion = ubicacion
        self.historial.append(ubicacion)

    def detectar_desvio(self, ruta: Ruta, tolerancia_m: float) -> bool:
        if self.ultima_ubicacion is None:
            raise ValueError("El bus aún no tiene ubicación GPS")
        return not ruta.esta_en_ruta(self.ultima_ubicacion, tolerancia_m)

    def actualizar_estado_por_ubicacion(
        self,
        ruta: Ruta,
        paradero: Paradero | None,
        tolerancia_desvio_m: float,
        tolerancia_paradero_m: float,
    ) -> EstadoBus:
        if tolerancia_paradero_m < 0:
            raise ValueError("tolerancia_paradero_m no puede ser negativa")
        if self.estado in (EstadoBus.EN_ESPERA, EstadoBus.FUERA_DE_SERVICIO):
            return self.estado
        if self.detectar_desvio(ruta, tolerancia_desvio_m):
            self.estado = EstadoBus.DESVIADO
        elif (
            paradero is not None
            and self.ultima_ubicacion is not None
            and paradero.distancia_a(self.ultima_ubicacion) <= tolerancia_paradero_m
        ):
            self.estado = EstadoBus.EN_PARADERO
        else:
            self.estado = EstadoBus.EN_RUTA
        return self.estado

    def estado_actual(self) -> EstadoBus:
        return self.estado

    def iniciar_servicio(self) -> None:
        if self.estado is EstadoBus.FUERA_DE_SERVICIO:
            raise ValueError("No se puede iniciar un bus fuera de servicio")
        self.estado = EstadoBus.EN_RUTA

    def retirar_servicio(self) -> None:
        self.estado = EstadoBus.FUERA_DE_SERVICIO


@dataclass(frozen=True, slots=True)
class ETA:
    bus_id: Id
    paradero_id: Id
    llegada_estimada: datetime
    calculada_en: datetime

    def vigente(self, ahora: datetime, antiguedad_max: timedelta) -> bool:
        edad = ahora - self.calculada_en
        return timedelta(0) <= edad <= antiguedad_max


@dataclass(frozen=True, slots=True)
class AlertaDesvio:
    id: Id
    bus_id: Id
    ubicacion: UbicacionGPS
    creada_en: datetime
    descripcion: str

    @staticmethod
    def desde_bus(
        bus: Bus,
        ubicacion: UbicacionGPS,
        creada_en: datetime,
    ) -> AlertaDesvio:
        return AlertaDesvio(
            id=Id(str(uuid4())),
            bus_id=bus.id,
            ubicacion=ubicacion,
            creada_en=creada_en,
            descripcion="La ubicación reciente está fuera del trazado asignado.",
        )
