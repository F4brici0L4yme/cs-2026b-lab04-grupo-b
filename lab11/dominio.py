"""Servicios de dominio mínimos que consume el adaptador MCP de RutaSIT."""

from __future__ import annotations

from typing import TypedDict


class BusEnRuta(TypedDict):
    bus_id: str
    ruta_id: str
    estado: str
    siguiente_paradero: str


class Llegada(TypedDict):
    bus_id: str
    paradero_id: str
    eta_min: float | None
    estado: str


_BUSES: tuple[BusEnRuta, ...] = (
    {"bus_id": "SIT-101", "ruta_id": "R-01", "estado": "EN_RUTA", "siguiente_paradero": "P-03"},
    {"bus_id": "SIT-102", "ruta_id": "R-01", "estado": "EN_PARADERO", "siguiente_paradero": "P-02"},
    {"bus_id": "SIT-201", "ruta_id": "R-02", "estado": "DESVIADO", "siguiente_paradero": "P-08"},
)
_LLEGADAS: dict[tuple[str, str], Llegada] = {
    ("SIT-101", "P-03"): {"bus_id": "SIT-101", "paradero_id": "P-03", "eta_min": 4.5, "estado": "ACTUAL"},
    ("SIT-102", "P-02"): {"bus_id": "SIT-102", "paradero_id": "P-02", "eta_min": 0.0, "estado": "ACTUAL"},
    ("SIT-201", "P-08"): {"bus_id": "SIT-201", "paradero_id": "P-08", "eta_min": None, "estado": "DESVIADO"},
}


def buses_en_ruta(ruta_id: str) -> list[BusEnRuta]:
    """Devuelve las unidades activas de una ruta publicada."""
    return [bus for bus in _BUSES if bus["ruta_id"] == ruta_id]


def tiempo_llegada(bus_id: str, paradero_id: str) -> Llegada:
    """Consulta el ETA materializado por bus y paradero."""
    return _LLEGADAS.get(
        (bus_id, paradero_id),
        {"bus_id": bus_id, "paradero_id": paradero_id, "eta_min": None, "estado": "SIN_DATOS"},
    )


def ids_bus() -> set[str]:
    return {bus["bus_id"] for bus in _BUSES}
