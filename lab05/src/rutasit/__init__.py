"""Esqueleto de dominio RutaSIT para el Laboratorio 05."""

from .compartido import Id
from .dominio import (
    AlertaDesvio,
    Bus,
    Conductor,
    EstadoBus,
    ETA,
    Paradero,
    Ruta,
    UbicacionGPS,
    UsuarioSistema,
)
from .servicios import MonitoreoController, ResultadoSeguimiento, RutaSITAPI, SeguimientoService

__all__ = [
    "AlertaDesvio",
    "Bus",
    "Conductor",
    "EstadoBus",
    "ETA",
    "Id",
    "MonitoreoController",
    "Paradero",
    "ResultadoSeguimiento",
    "Ruta",
    "RutaSITAPI",
    "SeguimientoService",
    "UbicacionGPS",
    "UsuarioSistema",
]
