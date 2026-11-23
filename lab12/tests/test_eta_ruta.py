"""HU-12: consulta pública de ETA según el trazado restante."""
from datetime import datetime, timezone

import pytest

from rutasit.compartido import Id
from rutasit.dominio import Bus, EstadoBus, Paradero, Ruta, UbicacionGPS
from rutasit.infraestructura import NotificadorAlertaMemoria, ProveedorGPSMemoria, RepositorioMemoria
from rutasit.servicios import SeguimientoService
from rutasit_lab12.eta_ruta import EstimadorETADeRuta, distancia_restante_m

AHORA = datetime(2026, 11, 23, tzinfo=timezone.utc)


def punto(lat: float, lon: float) -> UbicacionGPS:
    return UbicacionGPS(lat, lon, AHORA)


def preparar(ubicacion: UbicacionGPS) -> tuple[SeguimientoService, Bus, Paradero, ProveedorGPSMemoria]:
    paradero = Paradero(Id("p1"), "Centro", punto(-16.39, -71.53))
    ruta = Ruta(
        Id("r1"), "Curva", (paradero,),
        (punto(-16.4, -71.54), punto(-16.4, -71.53), punto(-16.39, -71.53),
         punto(-16.388, -71.53)),
    )
    bus = Bus(Id("b1"), ruta_id=ruta.id, estado=EstadoBus.EN_RUTA)
    bus.actualizar_ubicacion(ubicacion)
    repo = RepositorioMemoria(buses={bus.id: bus}, rutas={ruta.id: ruta}, paraderos={paradero.id: paradero})
    gps = ProveedorGPSMemoria({bus.id: ubicacion})
    estimator = EstimadorETADeRuta({ruta.id: ruta}, velocidad_media_m_s=10.0)
    service = SeguimientoService(repo, gps, NotificadorAlertaMemoria(), estimator, _RelojFijo())
    return service, bus, paradero, gps


class _RelojFijo:
    def ahora(self) -> datetime:
        return AHORA


def test_consulta_seguimiento_usa_distancia_de_la_curva() -> None:
    service, bus, paradero, _ = preparar(punto(-16.4, -71.539))

    resultado = service.consultar_seguimiento(bus.id, paradero.id)

    assert resultado.eta is not None
    assert 200 < (resultado.eta.llegada_estimada - AHORA).total_seconds() < 220


def test_consulta_seguimiento_da_llegada_inmediata_si_ya_paso() -> None:
    service, bus, paradero, _ = preparar(punto(-16.389, -71.53))

    resultado = service.consultar_seguimiento(bus.id, paradero.id)

    assert resultado.eta is not None
    assert resultado.eta.llegada_estimada == AHORA


def test_distancia_restante_rechaza_trazado_insuficiente() -> None:
    with pytest.raises(ValueError, match="dos puntos"):
        distancia_restante_m((punto(-16.4, -71.54),), punto(-16.4, -71.54), punto(-16.39, -71.53))


def test_gps_vencido_no_publica_eta() -> None:
    service, bus, paradero, gps = preparar(punto(-16.4, -71.539))
    viejo = UbicacionGPS(-16.4, -71.539, AHORA.replace(year=2020))
    bus.actualizar_ubicacion(viejo)
    gps.registrar(bus.id, viejo)

    resultado = service.consultar_seguimiento(bus.id, paradero.id)

    assert resultado.eta is None
    assert not resultado.telemetria_vigente



def test_estimador_retorna_none_si_bus_no_tiene_posicion() -> None:
    estimator = EstimadorETADeRuta({})
    bus = Bus(Id("b2"), ruta_id=Id("r1"))
    paradero = Paradero(Id("p2"), "Centro", punto(-16.39, -71.53))

    assert estimator.calcular_eta(bus, paradero, AHORA) is None


def test_estimador_rechaza_velocidad_no_positiva() -> None:
    with pytest.raises(ValueError, match="positiva"):
        EstimadorETADeRuta({}, velocidad_media_m_s=0)


def test_estimador_falla_si_no_existe_ruta() -> None:
    estimator = EstimadorETADeRuta({})
    bus = Bus(Id("b3"), ruta_id=Id("missing"))
    bus.actualizar_ubicacion(punto(-16.4, -71.539))
    paradero = Paradero(Id("p3"), "Centro", punto(-16.39, -71.53))

    with pytest.raises(ValueError, match="No existe la ruta"):
        estimator.calcular_eta(bus, paradero, AHORA)
