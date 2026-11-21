import pytest

from agentes.agente.contrato import validar_decision


HERRAMIENTAS = {"leer_archivo", "editar_archivo"}


@pytest.mark.parametrize(
    "decision,esperado",
    [
        ({"pensamiento": "leo", "accion": "leer_archivo", "args": {"ruta": "a.py"}}, True),
        ({"pensamiento": "terminé", "final": "Resuelto"}, True),
        ({"accion": "leer_archivo"}, False),
        ({"pensamiento": "x", "accion": "borrar_todo"}, False),
        ({"pensamiento": "x", "accion": "leer_archivo", "final": "y"}, False),
        ({"pensamiento": "x", "accion": "leer_archivo", "args": "a.py"}, False),
        ({"pensamiento": "x", "accion": "leer_archivo", "extra": 1}, False),
        ("leer_archivo(a.py)", False),
    ],
)
def test_contrato(decision, esperado):
    assert validar_decision(decision, HERRAMIENTAS)[0] is esperado
