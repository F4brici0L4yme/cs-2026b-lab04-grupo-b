"""Reglas mínimas de ETA, trazado GPS y respuesta sin señal de RutaSIT."""

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
    return round(max(0.0, distancia_m) / velocidad_m_s / 60, 2)


def esta_en_ruta(
    ubicacion: Punto,
    trazado: Sequence[Punto],
    tolerancia_m: float = 30.0,
) -> bool:
    if tolerancia_m < 0:
        raise ValueError("La tolerancia no puede ser negativa")
    if len(trazado) < 2:
        raise ValueError("El trazado requiere al menos dos puntos")
    distancias: list[float] = []
    for inicio, fin in zip(trazado, trazado[1:]):
        dx = fin.x_m - inicio.x_m
        dy = fin.y_m - inicio.y_m
        longitud2 = dx * dx + dy * dy
        if longitud2 == 0:
            distancia = hypot(ubicacion.x_m - inicio.x_m, ubicacion.y_m - inicio.y_m)
        else:
            numerador = (ubicacion.x_m - inicio.x_m) * dx + (ubicacion.y_m - inicio.y_m) * dy
            t = max(0.0, min(1.0, numerador / longitud2))
            x_cercano = inicio.x_m + t * dx
            y_cercano = inicio.y_m + t * dy
            distancia = hypot(ubicacion.x_m - x_cercano, ubicacion.y_m - y_cercano)
        distancias.append(distancia)
    return min(distancias) <= tolerancia_m


def crear_respuesta_gps(eta_min: float | None) -> dict[str, float | str | None]:
    if eta_min is None:
        return {"eta_min": None, "estado": "SIN_DATOS"}
    return {"eta_min": eta_min, "estado": "ACTUAL"}
