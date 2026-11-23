"""Cálculo de distancia restante sobre una polilínea de ruta."""
from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import datetime, timedelta

from rutasit.compartido import Id
from rutasit.dominio import Bus, ETA, Paradero, Ruta

from rutasit.dominio import UbicacionGPS

_RADIO_TIERRA_M = 6_371_000.0


def _proyectar(punto: UbicacionGPS, latitud_ref: float) -> tuple[float, float]:
    """Proyecta coordenadas a metros en un plano local equirectangular."""
    lat = math.radians(punto.latitud)
    lon = math.radians(punto.longitud)
    return (
        _RADIO_TIERRA_M * lon * math.cos(latitud_ref),
        _RADIO_TIERRA_M * lat,
    )


def _proyeccion_y_cadena(
    punto: UbicacionGPS, ruta: Sequence[UbicacionGPS], latitud_ref: float
) -> tuple[float, float]:
    """Retorna distancia al trazado y posición acumulada de su proyección más cercana."""
    px, py = _proyectar(punto, latitud_ref)
    proyectados = [_proyectar(p, latitud_ref) for p in ruta]
    acumulada = 0.0
    mejor_distancia = math.inf
    mejor_cadena = 0.0
    for (ax, ay), (bx, by) in zip(proyectados, proyectados[1:]):
        dx, dy = bx - ax, by - ay
        longitud = math.hypot(dx, dy)
        if longitud == 0:
            t = 0.0
            distancia = math.hypot(px - ax, py - ay)
        else:
            t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / longitud**2))
            distancia = math.hypot(px - (ax + t * dx), py - (ay + t * dy))
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_cadena = acumulada + t * longitud
        acumulada += longitud
    return mejor_distancia, mejor_cadena


def distancia_restante_m(
    puntos_trazado: Sequence[UbicacionGPS],
    ubicacion: UbicacionGPS,
    paradero: UbicacionGPS,
) -> float:
    """Estima metros restantes siguiendo la ruta y devuelve cero si ya pasó."""
    if len(puntos_trazado) < 2:
        raise ValueError("El trazado requiere al menos dos puntos")
    latitud_ref = math.radians(ubicacion.latitud)
    _, cadena_bus = _proyeccion_y_cadena(ubicacion, puntos_trazado, latitud_ref)
    distancia_paradero, cadena_paradero = _proyeccion_y_cadena(
        paradero, puntos_trazado, latitud_ref
    )
    if distancia_paradero > 100.0:
        raise ValueError("El paradero no está suficientemente cerca del trazado")
    return max(0.0, cadena_paradero - cadena_bus)


class EstimadorETADeRuta:
    """Implementa el puerto ETA existente usando el trazado del bus."""

    def __init__(self, rutas: dict[Id, Ruta], velocidad_media_m_s: float = 6.0) -> None:
        if velocidad_media_m_s <= 0:
            raise ValueError("La velocidad media debe ser positiva")
        self._rutas = rutas
        self._velocidad_media_m_s = velocidad_media_m_s

    def calcular_eta(self, bus: Bus, paradero: Paradero, calculada_en: datetime) -> ETA | None:
        if bus.ultima_ubicacion is None or bus.ruta_id is None:
            return None
        ruta = self._rutas.get(bus.ruta_id)
        if ruta is None:
            raise ValueError(f"No existe la ruta {bus.ruta_id}")
        distancia = distancia_restante_m(
            ruta.puntos_trazado, bus.ultima_ubicacion, paradero.ubicacion
        )
        llegada = calculada_en + timedelta(seconds=distancia / self._velocidad_media_m_s)
        return ETA(bus.id, paradero.id, llegada, calculada_en)
