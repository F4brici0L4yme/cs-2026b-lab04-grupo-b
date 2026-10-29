"""Datos de la unidad y reglas de vigencia (HU-06, Lab 05)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LecturaETA:
    bus_id: str
    paradero_id: str
    evento_id: int
    capturada_s: float
    eta_min: float

    def vigente(self, ahora: float) -> bool:
        return 0 <= ahora - self.capturada_s <= 30


@dataclass(frozen=True)
class Seguimiento:
    bus_id: str
    paradero_id: str
    eta_min: float | None
    edad_s: float | None
    estado: str
