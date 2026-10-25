"""Pagos adaptado a RutaSIT: Strategy (ETA) + Adapter (GPS) + Factory + Decorator."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Ubicacion:
    ok: bool
    lat: float | None = None
    lon: float | None = None


class EstrategiaETA(ABC):
    """Strategy: algoritmos de ETA intercambiables."""

    @abstractmethod
    def calcular(self, distancia_m: float) -> float: ...


class EstimadorBase(EstrategiaETA):
    def calcular(self, distancia_m):
        return round(distancia_m / 8.33 / 60, 2)


class EstimadorHoraPunta(EstrategiaETA):
    def calcular(self, distancia_m):
        return round(distancia_m / 4.16 / 60, 2)


class PuertoGPS(ABC):
    @abstractmethod
    def obtener_ubicacion(self, bus_id: str) -> Ubicacion: ...


class GpsAdapterA(PuertoGPS):
    """Adapter: traduce GpsOperadorA a PuertoGPS."""

    def __init__(self, sdk):
        self._sdk = sdk

    def obtener_ubicacion(self, bus_id):
        r = self._sdk.realizar_lectura(bus_id)
        return Ubicacion(r["ok"], r.get("lat"), r.get("lon"))


class GpsAdapterB(PuertoGPS):
    """Adapter: traduce GpsOperadorB a PuertoGPS."""

    def __init__(self, cliente):
        self._cliente = cliente

    def obtener_ubicacion(self, bus_id):
        codigo, lat, lon = self._cliente.fetch_position(bus_id)
        return Ubicacion(codigo == 200, lat, lon)


class ConReintentos(PuertoGPS):
    """Decorator: reintenta solo ante TimeoutError."""

    def __init__(self, interno: PuertoGPS, intentos: int = 3):
        self._interno, self._intentos = interno, intentos

    def obtener_ubicacion(self, bus_id):
        for _ in range(self._intentos):
            try:
                return self._interno.obtener_ubicacion(bus_id)
            except TimeoutError:
                continue
        return Ubicacion(False)


class FabricaGPS:
    """Factory (registro): crea la estrategia GPS por nombre."""

    def __init__(self, gps_a=None, gps_b=None):
        from .externos import GpsOperadorA, GpsOperadorB

        self._gps_a = gps_a or GpsOperadorA()
        self._gps_b = gps_b or GpsOperadorB()
        self._creadores = {
            "A": lambda: GpsAdapterA(self._gps_a),
            "B": lambda: GpsAdapterB(self._gps_b),
        }

    def registrar(self, nombre: str, creador):
        self._creadores[nombre] = creador

    def crear(self, nombre: str) -> PuertoGPS:
        if nombre not in self._creadores:
            raise ValueError(f"Proveedor GPS no soportado: {nombre}")
        return ConReintentos(self._creadores[nombre]())


class FabricaETAs:
    """Factory de algoritmos ETA."""

    def __init__(self):
        self._creadores = {"BASE": EstimadorBase, "PUNTA": EstimadorHoraPunta}

    def registrar(self, nombre: str, creador):
        self._creadores[nombre] = creador

    def crear(self, nombre: str) -> EstrategiaETA:
        if nombre not in self._creadores:
            raise ValueError(f"Algoritmo no soportado: {nombre}")
        return self._creadores[nombre]()
