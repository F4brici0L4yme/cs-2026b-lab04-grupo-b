"""Pruebas de caracterización: mismo comportamiento antes y después."""

import importlib

import pytest

from rutasit.externos import ClienteLLMFalso, GpsOperadorA


@pytest.fixture(params=["rutasit.antes.servicio", "rutasit.servicio"])
def m(request):
    return importlib.import_module(request.param)


def bus(m, **kw):
    base = {"id": "BUS-01", "estado": "EN_ESPERA", "edad_s": 5, "distancia_m": 10.0, "cerca_paradero": False}
    base.update(kw)
    return m.Bus(**base)


def test_ruta_ok_publica_eventos(m):
    s = m.ServicioSeguimiento()
    assert s.consultar_seguimiento(bus(m), "P-01", "A", "BASE") == "EN_RUTA"
    assert s.eventos == ["sms:BUS-01:En ruta ETA 0.02", "panel:BUS-01:0.02"]


def test_paradero_cercano(m):
    s = m.ServicioSeguimiento()
    assert s.consultar_seguimiento(bus(m, cerca_paradero=True), "P-01", "B", "BASE") == "EN_PARADERO"
    assert s.eventos[0].startswith("sms:BUS-01:Llegando a P-01")


def test_desvio_genera_alerta(m):
    s = m.ServicioSeguimiento()
    assert s.consultar_seguimiento(bus(m, distancia_m=50.0), "P-01", "A", "PUNTA") == "DESVIADO"
    assert len(s.eventos) == 2 and "Desv" in s.eventos[0]


def test_telemetria_antigua_no_cambia(m):
    s = m.ServicioSeguimiento()
    b = bus(m, edad_s=40)
    assert s.consultar_seguimiento(b, "P-01", "A", "BASE") == "EN_ESPERA"
    assert s.eventos == []


def test_fuera_de_servicio_lanza(m):
    s = m.ServicioSeguimiento()
    with pytest.raises(ValueError):
        s.consultar_seguimiento(bus(m, estado="FUERA_DE_SERVICIO"), "P-01", "A", "BASE")


def test_reintenta_tras_dos_timeouts(m):
    gps_a = GpsOperadorA(fallas=2)
    s = m.ServicioSeguimiento(gps_a=gps_a)
    assert s.consultar_seguimiento(bus(m), "P-01", "A", "BASE") == "EN_RUTA"
    assert gps_a.llamadas == 3


def test_sin_senal_sin_eventos(m):
    s = m.ServicioSeguimiento()
    assert s.consultar_seguimiento(bus(m, id="SIN_SENAL"), "P-01", "A", "BASE") == "EN_RUTA"
    assert s.eventos == []


def test_algoritmo_no_soportado(m):
    s = m.ServicioSeguimiento()
    with pytest.raises(ValueError, match="Algoritmo"):
        s.consultar_seguimiento(bus(m), "P-01", "A", "NOEXISTE")


def test_proveedor_no_soportado_no_altera_estado(m):
    s = m.ServicioSeguimiento()
    b = bus(m)
    with pytest.raises(ValueError, match="Proveedor GPS"):
        s.consultar_seguimiento(b, "P-01", "Z", "BASE")
    if m.__name__ == "rutasit.antes.servicio":
        assert b.estado == "EN_RUTA"
        pytest.xfail("bug documentado: antes deja EN_RUTA aunque falle")
    assert b.estado == "EN_ESPERA"


def test_ia_explica_ok(m):
    s = m.ServicioSeguimiento()
    assert "congestión" in s.explicar_retraso("bus 12 tarde", "FAKE")


def test_ia_bloquea_precio(m):
    s = m.ServicioSeguimiento(llm=ClienteLLMFalso("cuesta S/ 2.50"))
    with pytest.raises(ValueError, match="precio"):
        s.explicar_retraso("bus 12 tarde", "FAKE")


def test_ia_bloquea_afirmacion(m):
    s = m.ServicioSeguimiento(llm=ClienteLLMFalso("cura garantizado el tráfico"))
    with pytest.raises(ValueError, match="afirmación"):
        s.explicar_retraso("bus 12 tarde", "FAKE")
