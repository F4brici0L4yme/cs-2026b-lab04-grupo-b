"""Contratos del servidor MCP sin LLM ni red."""

from __future__ import annotations

import asyncio

from mcp.client import Client

from servidor_mcp import rutasit_mcp as srv


def correr(fn):
    async def ejecutar():
        async with Client(srv.mcp, mode="2026-07-28", read_timeout_seconds=5) as cliente:
            return await fn(cliente)
    return asyncio.run(ejecutar())


def texto(resultado) -> str:
    return " ".join(getattr(bloque, "text", "") for bloque in resultado.content)


def test_catalogo_estable_y_documentado():
    herramientas = correr(lambda c: c.list_tools()).tools
    assert [h.name for h in herramientas] == ["buses_en_ruta", "tiempo_llegada", "reportar_desvio"]
    assert all(h.description and len(h.description) > 35 for h in herramientas)
    assert all(h.input_schema["type"] == "object" for h in herramientas)


def test_minimo_privilegio_una_sola_escritura():
    herramientas = correr(lambda c: c.list_tools()).tools
    escritura = [h.name for h in herramientas if not h.annotations.read_only_hint]
    assert escritura == ["reportar_desvio"]


def test_buses_en_ruta_devuelve_datos_acotados():
    resultado = correr(lambda c: c.call_tool("buses_en_ruta", {"ruta_id": "R-01"}))
    assert not resultado.is_error
    assert len(resultado.structured_content["result"]) == 2


def test_tiempo_llegada_publica_salida_estructurada():
    resultado = correr(lambda c: c.call_tool("tiempo_llegada", {"bus_id": "SIT-101", "paradero_id": "P-03"}))
    assert not resultado.is_error
    assert resultado.structured_content == {"bus_id": "SIT-101", "paradero_id": "P-03", "eta_min": 4.5, "estado": "ACTUAL"}


def test_bus_invalido_devuelve_error_corregible():
    resultado = correr(lambda c: c.call_tool("tiempo_llegada", {"bus_id": "SIT-999", "paradero_id": "P-03"}))
    assert resultado.is_error
    assert "Valores válidos" in texto(resultado)


def test_paradero_invalido_explica_formato():
    resultado = correr(lambda c: c.call_tool("tiempo_llegada", {"bus_id": "SIT-101", "paradero_id": "3"}))
    assert resultado.is_error
    assert "P-NN" in texto(resultado)


def test_reporte_solo_crea_archivos_nuevos(tmp_path, monkeypatch):
    monkeypatch.setattr(srv, "RAIZ", tmp_path)
    for _ in range(2):
        resultado = correr(lambda c: c.call_tool("reportar_desvio", {
            "bus_id": "SIT-201", "ruta_id": "R-02",
            "descripcion": "GPS confirma ubicación fuera del trazado junto al puente principal.",
        }))
        assert not resultado.is_error
    assert [p.name for p in sorted((tmp_path / "reportes").iterdir())] == ["DESVIO-01.md", "DESVIO-02.md"]


def test_reporte_rechaza_evidencia_demasiado_corta():
    resultado = correr(lambda c: c.call_tool("reportar_desvio", {
        "bus_id": "SIT-201", "ruta_id": "R-02", "descripcion": "Desvío.",
    }))
    assert resultado.is_error
    assert "20 y 500" in texto(resultado)


def test_reporte_publica_limite_de_texto_en_el_contrato():
    herramienta = next(h for h in correr(lambda c: c.list_tools()).tools if h.name == "reportar_desvio")
    schema = herramienta.input_schema["properties"]["descripcion"]
    assert schema["minLength"] == 20
    assert schema["maxLength"] == 500


def test_recurso_plantilla_rechaza_ruta():
    with __import__("pytest").raises(Exception):
        correr(lambda c: c.read_resource("rutasit://adr/../../secretos"))


def test_recursos_y_prompt_se_descubren():
    recursos = correr(lambda c: c.list_resources()).resources
    plantillas = correr(lambda c: c.list_resource_templates()).resource_templates
    prompts = correr(lambda c: c.list_prompts()).prompts
    assert {r.uri for r in recursos} == {"rutasit://mapa/rutas", "rutasit://reglas/operacion"}
    assert [p.uri_template for p in plantillas] == ["rutasit://adr/{numero}"]
    assert [p.name for p in prompts] == ["aviso_usuarios"]
