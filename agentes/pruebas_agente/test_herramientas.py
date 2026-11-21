from pathlib import Path

import pytest

from agentes.agente.herramientas import Herramientas


def test_ruta_no_sale_del_sandbox(tmp_path):
    herramientas = Herramientas(tmp_path)
    with pytest.raises(PermissionError):
        herramientas._ruta("../../etc/passwd")


def test_edicion_exige_una_ocurrencia(tmp_path):
    archivo = tmp_path / "sample.py"
    archivo.write_text("x = 1\nx = 1\n", encoding="utf-8")
    herramientas = Herramientas(tmp_path)
    assert "aparece 2 veces" in herramientas.editar_archivo(
        "sample.py", "x = 1", "x = 2"
    )
    assert archivo.read_text(encoding="utf-8") == "x = 1\nx = 1\n"


def test_listar_y_buscar_solo_archivos_del_sandbox(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("def ETA():\n    return 1\n", encoding="utf-8")
    herramientas = Herramientas(tmp_path)
    assert "src/a.py" in herramientas.listar_archivos("src")
    assert "src/a.py:1" in herramientas.buscar("ETA", "src")


def test_mapa_repo_extrae_clases_y_firmas_con_ast(tmp_path):
    modulo = tmp_path / "src" / "rutasit.py"
    modulo.parent.mkdir()
    modulo.write_text(
        "class Bus:\n"
        "    def estado(self, ahora: int = 0) -> str:\n"
        "        return 'EN_RUTA'\n"
        "def calcular_eta(distancia: float) -> float:\n"
        "    return distancia\n",
        encoding="utf-8",
    )
    resultado = Herramientas(tmp_path).mapa_repo("src")
    assert "class Bus" in resultado
    assert "def estado(self, ahora: int=0)" in resultado
    assert "def calcular_eta(distancia: float)" in resultado


def test_memoria_no_escapa_del_sandbox_por_symlink(tmp_path):
    afuera = tmp_path.parent / f"{tmp_path.name}-afuera.md"
    afuera.write_text("no sobrescribir", encoding="utf-8")
    (tmp_path / "agentes").mkdir()
    (tmp_path / "agentes/notas.md").symlink_to(afuera)
    with pytest.raises(PermissionError):
        Herramientas(tmp_path)


def test_memoria_no_duplica_notas(tmp_path):
    herramientas = Herramientas(tmp_path)
    nota = "hipótesis de una ejecución"
    assert herramientas.anotar(nota) == "OK: nota guardada"
    assert herramientas.anotar(nota) == "OK: nota ya registrada"
    assert herramientas.leer_notas().splitlines() == [f"- {nota}"]
