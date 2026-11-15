"""Generación estructurada a través del puerto ProveedorLLM."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import ValidationError, validate

from .ia import ProveedorLLM


class SalidaInvalida(ValueError):
    """La respuesta no es JSON válido o incumple el esquema de la tarea."""


class GeneradorPrompt:
    def __init__(self, proveedor: ProveedorLLM, prompts_dir: Path, tarea: str, version: str = "v3"):
        self.proveedor = proveedor
        self.plantilla = (prompts_dir / tarea / f"{version}.txt").read_text(encoding="utf-8")
        self.esquema = json.loads((prompts_dir / tarea / "esquema.json").read_text(encoding="utf-8"))
        self.version = version

    def generar(self, identificador: str, entrada: str) -> dict:
        prompt = self.plantilla.replace("{{id}}", identificador).replace("{{historia}}", entrada).replace("{{codigo}}", entrada)
        try:
            salida = json.loads(self.proveedor.completar(prompt))
            validate(instance=salida, schema=self.esquema)
        except (json.JSONDecodeError, ValidationError) as error:
            raise SalidaInvalida(f"{self.version}/{identificador}: {error}") from error
        return salida
