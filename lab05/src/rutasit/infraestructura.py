"""Adaptadores en memoria para ejecutar y probar el esqueleto sin servicios externos."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .compartido import Id
from .dominio import AlertaDesvio, Bus, ETA, Paradero, Ruta, UbicacionGPS


class RepositorioMemoria:
    def __init__(
        self,
        buses: dict[Id, Bus] | None = None,
        rutas: dict[Id, Ruta] | None = None,
        paraderos: dict[Id, Paradero] | None = None,
    ) -> None:
        self._buses = dict(buses or {})
        self._rutas = dict(rutas or {})
        self._paraderos = dict(paraderos or {})

    def obtener_bus(self, bus_id: Id) -> Bus:
        try:
            return self._buses[bus_id]
        except KeyError as exc:
            raise KeyError(f"Bus no encontrado: {bus_id}") from exc

    def obtener_ruta(self, ruta_id: Id) -> Ruta:
        try:
            return self._rutas[ruta_id]
        except KeyError as exc:
            raise KeyError(f"Ruta no encontrada: {ruta_id}") from exc

    def obtener_paradero(self, paradero_id: Id) -> Paradero:
        try:
            return self._paraderos[paradero_id]
        except KeyError as exc:
            raise KeyError(f"Paradero no encontrado: {paradero_id}") from exc

    def guardar_bus(self, bus: Bus) -> None:
        self._buses[bus.id] = bus


class ProveedorGPSMemoria:
    def __init__(self, ubicaciones: dict[Id, UbicacionGPS] | None = None) -> None:
        self._ubicaciones = dict(ubicaciones or {})

    def obtener_ultima_ubicacion(self, bus_id: Id) -> UbicacionGPS:
        try:
            return self._ubicaciones[bus_id]
        except KeyError as exc:
            raise KeyError(f"No hay telemetría para el bus {bus_id}") from exc

    def registrar(self, bus_id: Id, ubicacion: UbicacionGPS) -> None:
        self._ubicaciones[bus_id] = ubicacion


class NotificadorAlertaMemoria:
    def __init__(self) -> None:
        self.alertas: list[AlertaDesvio] = []

    def notificar(self, alerta: AlertaDesvio) -> None:
        # Representa la aceptación asíncrona por una cola, no el envío push final.
        self.alertas.append(alerta)


class EstimadorETASimple:
    def __init__(self, velocidad_media_m_s: float = 6.0) -> None:
        if velocidad_media_m_s <= 0:
            raise ValueError("La velocidad media debe ser positiva")
        self._velocidad_media_m_s = velocidad_media_m_s

    def calcular_eta(
        self,
        bus: Bus,
        paradero: Paradero,
        calculada_en: datetime,
    ) -> ETA | None:
        if bus.ultima_ubicacion is None:
            return None
        distancia = paradero.distancia_a(bus.ultima_ubicacion)
        segundos = distancia / self._velocidad_media_m_s
        return ETA(
            bus_id=bus.id,
            paradero_id=paradero.id,
            llegada_estimada=calculada_en + timedelta(seconds=segundos),
            calculada_en=calculada_en,
        )


class RelojSistema:
    def ahora(self) -> datetime:
        return datetime.now(timezone.utc)
