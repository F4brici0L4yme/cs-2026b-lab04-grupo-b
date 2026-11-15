import json
from pathlib import Path

import pytest

from rutasit.generador_prompt import GeneradorPrompt, SalidaInvalida


class ProveedorGrabado:
    def __init__(self, salida: str):
        self.salida = salida
        self.ultimo_prompt = ""

    def completar(self, prompt: str) -> str:
        self.ultimo_prompt = prompt
        return self.salida


def preparar_prompts(tmp_path: Path) -> Path:
    task = tmp_path / "pytest"
    task.mkdir()
    (task / "v3.txt").write_text("Pruebas para {{id}}: {{codigo}}", encoding="utf-8")
    (task / "esquema.json").write_text(json.dumps({
        "type": "object",
        "required": ["caso_id", "pruebas"],
        "additionalProperties": False,
        "properties": {"caso_id": {"type": "string"}, "pruebas": {"type": "string", "minLength": 10}},
    }), encoding="utf-8")
    return tmp_path


def test_acepta_respuesta_valida_y_sustituye_plantilla(tmp_path):
    proveedor = ProveedorGrabado(json.dumps({"caso_id": "E1", "pruebas": "def test_eta(): assert True"}))
    generador = GeneradorPrompt(proveedor, preparar_prompts(tmp_path), "pytest")
    respuesta = generador.generar("E1", "def calcular(d): return d / 60")
    assert respuesta["caso_id"] == "E1"
    assert "E1" in proveedor.ultimo_prompt
    assert "calcular" in proveedor.ultimo_prompt


def test_rechaza_json_malformado(tmp_path):
    generador = GeneradorPrompt(ProveedorGrabado("no json"), preparar_prompts(tmp_path), "pytest")
    with pytest.raises(SalidaInvalida, match="v3/E1"):
        generador.generar("E1", "def calcular(d): return d / 60")


def test_rechaza_json_que_no_cumple_esquema(tmp_path):
    generador = GeneradorPrompt(ProveedorGrabado('{"caso_id":"E1"}'), preparar_prompts(tmp_path), "pytest")
    with pytest.raises(SalidaInvalida):
        generador.generar("E1", "def calcular(d): return d / 60")
