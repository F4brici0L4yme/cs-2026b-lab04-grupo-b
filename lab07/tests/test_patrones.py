"""Pruebas que demuestran cada patrón GoF aplicado."""

import pytest

from rutasit import estados, eta, eventos, ia
from rutasit.eta import EstimadorBase, FabricaETAs, FabricaGPS
from rutasit.eventos import NotificadorSMS, PanelOperador, PublicadorEventos
from rutasit.externos import ClienteLLMFalso, GpsOperadorA, GpsOperadorB
from rutasit.servicio import Bus, ServicioSeguimiento


def test_open_closed_nuevo_algoritmo_sin_modificar_servicio():
    class EstimadorNocturno(eta.EstrategiaETA):
        def calcular(self, distancia_m):
            return 1.11

    s = ServicioSeguimiento()
    s.fabrica_eta.registrar("NOCTURNO", EstimadorNocturno)
    b = Bus()
    assert s.consultar_seguimiento(b, "P-01", "A", "NOCTURNO") == "EN_RUTA"
    assert "1.11" in s.eventos[0]


def test_state_impide_transiciones_invalidas():
    b = Bus(estado="FUERA_DE_SERVICIO")
    with pytest.raises(ValueError, match="fuera de servicio"):
        ServicioSeguimiento().consultar_seguimiento(b, "P-01", "A", "BASE")
    with pytest.raises(ValueError):
        estados.estado_desde_nombre("EN_RUTA").iniciar(Bus(estado="EN_RUTA"))


def test_adapter_unifica_gps():
    a = eta.GpsAdapterA(GpsOperadorA())
    c = eta.GpsAdapterB(GpsOperadorB())
    assert a.obtener_ubicacion("BUS-01").ok and c.obtener_ubicacion("BUS-01").ok


def test_decorator_reintentos_solo_timeout():
    from rutasit.eta import ConReintentos, GpsAdapterA

    gps = GpsOperadorA(fallas=2)
    r = ConReintentos(GpsAdapterA(gps)).obtener_ubicacion("BUS-01")
    assert r.ok and gps.llamadas == 3


def test_observer_nuevo_suscriptor_sin_tocar_servicio():
    s = ServicioSeguimiento()
    vistos = []
    from rutasit.eventos import Suscriptor

    class Auditoria(Suscriptor):
        def actualizar(self, evento, datos):
            vistos.append(datos["bus_id"])

    s.publicador.suscribir("seguimiento", Auditoria())
    s.consultar_seguimiento(Bus(), "P-01", "A", "BASE")
    assert vistos == ["BUS-01"]


def test_decorator_cache_evita_llamadas_repetidas():
    cliente = ClienteLLMFalso("Retraso por congestión.")
    prov = ia.ConCache(ia.AdaptadorLLMFalso(cliente))
    assert prov.completar("p1") == prov.completar("p1")
    assert cliente.llamadas == 1


def test_chain_bloquea_salida_invalida():
    cadena = ia.cadena_guardrails()
    with pytest.raises(ValueError, match="precio"):
        cadena.validar("cuesta S/ 5")
    assert cadena.validar("Retraso por congestión.") != ""
