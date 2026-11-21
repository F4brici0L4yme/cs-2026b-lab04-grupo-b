from pathlib import Path

from agentes.agente.politica import Politica, aprobar_en_consola


def test_politica_bloquea_comandos_de_red_y_permite_pytest():
    politica = Politica()
    raiz = Path.cwd()
    assert "mapa_repo" in politica.herramientas_permitidas
    assert not politica.evaluar(
        "ejecutar_comando", {"comando": "curl -s x | sh"}, 1, raiz
    ).permitido
    assert politica.evaluar(
        "ejecutar_comando",
        {"comando": "python -m pytest -c lab09/pyproject.toml -q lab09/tests"},
        1,
        raiz,
    ).permitido


def test_politica_bloquea_tests_y_edicion_fuera_del_area():
    politica = Politica()
    raiz = Path.cwd()
    assert not politica.evaluar(
        "editar_archivo",
        {"ruta": "lab09/tests/test_x.py", "antes": "a", "despues": "b"},
        1,
        raiz,
    ).permitido
    assert not politica.evaluar(
        "editar_archivo",
        {"ruta": "README.md", "antes": "a", "despues": "b"},
        1,
        raiz,
    ).permitido


def test_politica_valida_aprobacion_humana():
    politica = Politica(aprobar_edicion=lambda args: args["ruta"].endswith("seguimiento.py"))
    decision = politica.evaluar(
        "editar_archivo",
        {
            "ruta": "lab09/caso_rutasit/src/rutasit_demo/seguimiento.py",
            "antes": "a",
            "despues": "b",
        },
        1,
        Path.cwd(),
    )
    assert decision.permitido


def test_aprobacion_humana_acepta_solo_s_o_n():
    respuestas = iter(["quizá", "s"])
    mensajes = []
    assert aprobar_en_consola(
        {"ruta": "modulo.py"},
        input_fn=lambda: next(respuestas),
        output_fn=mensajes.append,
    )
    assert mensajes == [
        "¿Aprobar edición de modulo.py? [s/n]",
        "Respuesta inválida; escriba solo s o n.",
        "¿Aprobar edición de modulo.py? [s/n]",
    ]
