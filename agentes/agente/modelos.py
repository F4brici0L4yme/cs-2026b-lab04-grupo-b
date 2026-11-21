"""Estrategias de decisión grabada e interactiva, ambas sin dependencia de API."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol


class Modelo(Protocol):
    def decidir(self, historial: list[dict[str, str]]) -> object: ...


class ModeloGrabado:
    def __init__(self, decisiones: list[object] | Path):
        if isinstance(decisiones, Path):
            datos = json.loads(decisiones.read_text(encoding="utf-8"))
            decisiones = datos["decisiones"]
        self._decisiones = list(decisiones)
        self._indice = 0

    def decidir(self, historial: list[dict[str, str]]) -> object:
        del historial
        if self._indice >= len(self._decisiones):
            return {
                "pensamiento": "La trayectoria grabada terminó.",
                "final": "La trayectoria grabada terminó sin decisión final.",
            }
        decision = self._decisiones[self._indice]
        self._indice += 1
        return decision


class ModeloInteractivo:
    def __init__(self, input_fn=input, output_fn=print):
        self._input = input_fn
        self._output = output_fn

    def decidir(self, historial: list[dict[str, str]]) -> object:
        self._output("Contexto para el asistente externo:")
        for mensaje in historial[-8:]:
            self._output(f"{mensaje['role']}: {mensaje['content'][:1200]}")
        self._output("Pegue una decisión JSON de una sola línea:")
        respuesta = self._input()
        try:
            return json.loads(respuesta)
        except json.JSONDecodeError:
            return respuesta
