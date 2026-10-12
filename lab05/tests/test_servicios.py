from datetime import datetime, timedelta, timezone
import unittest

from rutasit.compartido import Id
from rutasit.dominio import Bus, EstadoBus, Paradero, Ruta, UbicacionGPS
from rutasit.infraestructura import (
    EstimadorETASimple,
    NotificadorAlertaMemoria,
    ProveedorGPSMemoria,
    RepositorioMemoria,
)
from rutasit.servicios import SeguimientoService


class RelojFijo:
    def __init__(self, momento: datetime) -> None:
        self._momento = momento

    def ahora(self) -> datetime:
        return self._momento


class SeguimientoServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ahora = datetime(2026, 10, 7, 12, 0, tzinfo=timezone.utc)
        self.ubicacion = UbicacionGPS(-16.3988, -71.5369, self.ahora)
        self.paradero = Paradero(Id("p-01"), "Paradero Centro", self.ubicacion)
        self.ruta = Ruta(
            Id("r-01"),
            "Ruta Centro",
            (self.paradero,),
            (
                UbicacionGPS(-16.3988, -71.5369, self.ahora),
                UbicacionGPS(-16.4000, -71.5350, self.ahora),
            ),
        )
        self.bus = Bus(Id("bus-01"), ruta_id=self.ruta.id)
        self.bus.iniciar_servicio()
        self.repositorio = RepositorioMemoria(
            buses={self.bus.id: self.bus},
            rutas={self.ruta.id: self.ruta},
            paraderos={self.paradero.id: self.paradero},
        )
        self.gps = ProveedorGPSMemoria({self.bus.id: self.ubicacion})
        self.notificador = NotificadorAlertaMemoria()
        self.service = SeguimientoService(
            self.repositorio,
            self.gps,
            self.notificador,
            EstimadorETASimple(),
            RelojFijo(self.ahora),
        )

    def test_consulta_en_ruta_devuelve_eta(self) -> None:
        resultado = self.service.consultar_seguimiento(self.bus.id, self.paradero.id)
        self.assertTrue(resultado.telemetria_vigente)
        self.assertIs(resultado.estado, EstadoBus.EN_PARADERO)
        self.assertIsNotNone(resultado.eta)
        self.assertIsNone(resultado.alerta)

    def test_desvio_notifica_solo_en_la_transicion(self) -> None:
        ubicacion = UbicacionGPS(-16.4100, -71.5200, self.ahora)
        self.gps.registrar(self.bus.id, ubicacion)
        primero = self.service.consultar_seguimiento(self.bus.id, self.paradero.id)
        segundo = self.service.consultar_seguimiento(self.bus.id, self.paradero.id)
        self.assertIs(primero.estado, EstadoBus.DESVIADO)
        self.assertIsNotNone(primero.alerta)
        self.assertIsNone(segundo.alerta)
        self.assertEqual(len(self.notificador.alertas), 1)

    def test_telemetria_obsoleta_no_cambia_estado_ni_notifica(self) -> None:
        antigua = UbicacionGPS(
            -16.4100,
            -71.5200,
            self.ahora - timedelta(minutes=2),
        )
        self.gps.registrar(self.bus.id, antigua)
        resultado = self.service.consultar_seguimiento(self.bus.id, self.paradero.id)
        self.assertFalse(resultado.telemetria_vigente)
        self.assertIs(self.bus.estado, EstadoBus.EN_RUTA)
        self.assertEqual(self.notificador.alertas, [])

    def test_bus_en_espera_no_publica_eta_ni_alerta(self) -> None:
        self.bus.estado = EstadoBus.EN_ESPERA
        resultado = self.service.consultar_seguimiento(self.bus.id, self.paradero.id)
        self.assertIs(resultado.estado, EstadoBus.EN_ESPERA)
        self.assertIsNone(resultado.eta)
        self.assertIsNone(resultado.alerta)
        self.assertEqual(self.notificador.alertas, [])


if __name__ == "__main__":
    unittest.main()
