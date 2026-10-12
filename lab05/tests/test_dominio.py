from datetime import datetime, timedelta, timezone
import unittest

from rutasit.compartido import Id
from rutasit.dominio import Bus, EstadoBus, Paradero, Ruta, UbicacionGPS


class DominioBusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ahora = datetime(2026, 10, 7, 12, 0, tzinfo=timezone.utc)
        self.paradero = Paradero(
            id=Id("p-01"),
            nombre="Paradero Centro",
            ubicacion=UbicacionGPS(-16.3988, -71.5369, self.ahora),
        )
        self.ruta = Ruta(
            id=Id("r-01"),
            nombre="Ruta Centro",
            paraderos=(self.paradero,),
            puntos_trazado=(
                UbicacionGPS(-16.3988, -71.5369, self.ahora),
                UbicacionGPS(-16.4000, -71.5350, self.ahora),
            ),
        )
        self.bus = Bus(id=Id("bus-01"), ruta_id=self.ruta.id)

    def test_distancia_a_si_misma_es_cero(self) -> None:
        self.assertAlmostEqual(self.paradero.ubicacion.distancia_a(self.paradero.ubicacion), 0.0)

    def test_ubicacion_vigente_dentro_de_tolerancia_marca_en_paradero(self) -> None:
        self.bus.iniciar_servicio()
        self.bus.actualizar_ubicacion(self.paradero.ubicacion)
        estado = self.bus.actualizar_estado_por_ubicacion(self.ruta, self.paradero, 30.0, 15.0)
        self.assertIs(estado, EstadoBus.EN_PARADERO)

    def test_ubicacion_fuera_del_trazado_marca_desvio(self) -> None:
        self.bus.iniciar_servicio()
        lejos = UbicacionGPS(-16.4100, -71.5200, self.ahora)
        self.bus.actualizar_ubicacion(lejos)
        estado = self.bus.actualizar_estado_por_ubicacion(self.ruta, self.paradero, 30.0, 15.0)
        self.assertIs(estado, EstadoBus.DESVIADO)

    def test_ubicacion_antigua_no_es_reciente(self) -> None:
        ubicacion = UbicacionGPS(-16.3988, -71.5369, self.ahora - timedelta(minutes=1))
        self.assertFalse(ubicacion.es_reciente(self.ahora, timedelta(seconds=30)))

    def test_bus_fuera_de_servicio_no_actualiza_estado(self) -> None:
        self.bus.retirar_servicio()
        estado = self.bus.actualizar_estado_por_ubicacion(self.ruta, self.paradero, 30.0, 15.0)
        self.assertIs(estado, EstadoBus.FUERA_DE_SERVICIO)

    def test_bus_en_espera_no_inicia_servicio_por_recibir_gps(self) -> None:
        self.bus.actualizar_ubicacion(self.paradero.ubicacion)
        estado = self.bus.actualizar_estado_por_ubicacion(self.ruta, self.paradero, 30.0, 15.0)
        self.assertIs(estado, EstadoBus.EN_ESPERA)


if __name__ == "__main__":
    unittest.main()
