from __future__ import annotations

from dataclasses import dataclass
from math import hypot
from typing import Sequence


@dataclass(frozen=True)
class Punto:
    x_m: float
    y_m: float


def calcular_eta_minutos(distancia_m: float, velocidad_m_s: float) -> float:
    if velocidad_m_s <= 0:
        raise ValueError("La velocidad debe ser positiva")
    return round(distancia_m / velocidad_m_s / 60, 2)


def esta_en_ruta(
    ubicacion: Punto,
    trazado: Sequence[Punto],
    tolerancia_m: float = 30.0,
) -> bool:
    if tolerancia_m < 0:
        raise ValueError("La tolerancia no puede ser negativa")
    if len(trazado) < 2:
        raise ValueError("El trazado requiere al menos dos puntos")
    return min(hypot(ubicacion.x_m - p.x_m, ubicacion.y_m - p.y_m) for p in trazado) <= tolerancia_m


def crear_respuesta_gps(eta_min: float | None) -> dict[str, float | str | None]:
    return {"eta_min": eta_min, "estado": "ACTUAL"}
