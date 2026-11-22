from agentes.reproducir import restablecer_funcion_inicial


def test_restaurar_funcion_no_cambia_las_otras_correcciones(tmp_path):
    (tmp_path / "lab10/caso_rutasit/src/rutasit_demo").mkdir(parents=True)
    (tmp_path / "lab10/caso_rutasit/fixtures").mkdir(parents=True)
    actual = tmp_path / "lab10/caso_rutasit/src/rutasit_demo/seguimiento.py"
    base = tmp_path / "lab10/caso_rutasit/fixtures/seguimiento_inicial.py"
    actual.write_text(
        "def eta():\n    return 0\n\n"
        "def ruta():\n    return True\n\n"
        "def gps():\n    return 'SIN_DATOS'\n",
        encoding="utf-8",
    )
    base.write_text(
        "def eta():\n    return -1\n\n"
        "def ruta():\n    return False\n\n"
        "def gps():\n    return 'ACTUAL'\n",
        encoding="utf-8",
    )

    restablecer_funcion_inicial(tmp_path, "ruta")

    texto = actual.read_text(encoding="utf-8")
    assert "def eta():\n    return 0" in texto
    assert "def ruta():\n    return False" in texto
    assert "def gps():\n    return 'SIN_DATOS'" in texto
