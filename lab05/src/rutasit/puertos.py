"""Puertos de aplicación; las capas externas proporcionan sus adaptadores."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from .compartido import Id
from .dominio import AlertaDesvio, Bus, ETA, Paradero, Ruta, UbicacionGPS


class IRepositorioRutaSIT(Protocol):
    def obtener_bus(self, bus_id: Id) -> Bus: ...

    def obtener_ruta(self, ruta_id: Id) -> Ruta: ...

    def obtener_paradero(self, paradero_id: Id) -> Paradero: ...

    def guardar_bus(self, bus: Bus) -> None: ...


class IGpsProvider(Protocol):
    def obtener_ultima_ubicacion(self, bus_id: Id) -> UbicacionGPS: ...


class INotificadorAlerta(Protocol):
    """El adaptador debe encolar el aviso y retornar sin bloquear el caso de uso."""

    def notificar(self, alerta: AlertaDesvio) -> None: ...


class IEstimadorETA(Protocol):
    def calcular_eta(
        self,
        bus: Bus,
        paradero: Paradero,
        calculada_en: datetime,
    ) -> ETA | None: ...


class IReloj(Protocol):
    def ahora(self) -> datetime: ...
