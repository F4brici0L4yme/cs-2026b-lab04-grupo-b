import json
from pathlib import Path

from agentes.agente.herramientas import Herramientas
from agentes.agente.modelos import ModeloGrabado
from agentes.agente.nucleo import Agente
from agentes.agente.politica import Politica


def test_agente_rechaza_decision_invalida_y_continua(tmp_path):
    root = tmp_path
    (root / "lab09/caso_rutasit/src").mkdir(parents=True)
    (root / "lab09/caso_rutasit/src/a.py").write_text("valor = 1\n", encoding="utf-8")
    decisions = [
        {"accion": "leer_archivo"},
        {"pensamiento": "termino", "final": "Prueba del contrato"},
    ]
    trace = root / "agentes/trazas/agente.jsonl"
    agent = Agente(
        "test",
        ModeloGrabado(decisions),
        Herramientas(root),
        Politica(max_pasos=3),
        "validar el contrato",
        trace,
    )
    assert "contrato" in agent.ejecutar().lower()
    events = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
    assert events[0]["estado"] == "CONTRATO_INVALIDO"
    assert events[1]["estado"] == "FINALIZADO"


def test_agente_politica_bloquea_edicion_de_pruebas(tmp_path):
    root = tmp_path
    (root / "lab09/tests").mkdir(parents=True)
    (root / "lab09/tests/test_x.py").write_text("x = 1\n", encoding="utf-8")
    decisions = [
        {
            "pensamiento": "intento editar una prueba",
            "accion": "editar_archivo",
            "args": {"ruta": "lab09/tests/test_x.py", "antes": "1", "despues": "2"},
        },
        {"pensamiento": "termino", "final": "La política bloqueó la edición."},
    ]
    trace = root / "agentes/trazas/bloqueo.jsonl"
    agent = Agente(
        "test",
        ModeloGrabado(decisions),
        Herramientas(root),
        Politica(max_pasos=3),
        "no edites pruebas",
        trace,
    )
    agent.ejecutar()
    events = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
    assert events[0]["estado"] == "BLOQUEADO"
    assert "Ruta protegida" in events[0]["observacion"]
