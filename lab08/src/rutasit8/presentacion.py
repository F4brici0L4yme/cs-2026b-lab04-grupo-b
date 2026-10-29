"""Representación pública sin datos del conductor (QA-05)."""

from dataclasses import asdict

from rutasit8.aplicacion.seguimiento import VistaSeguimiento


def consultar(vista: VistaSeguimiento, bus_id: str, paradero_id: str) -> dict:
    respuesta = vista.mostrar(bus_id, paradero_id)
    respuesta["seguimiento"] = asdict(respuesta["seguimiento"])
    return respuesta
