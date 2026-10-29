"""El ETA se consulta independientemente del proveedor de mapas."""

from rutasit8.aplicacion.puertos import Mapas, RepositorioETA
from rutasit8.dominio import Seguimiento


class ConsultaSeguimiento:
    def __init__(self, repositorio: RepositorioETA, reloj):
        self.repositorio, self.reloj = repositorio, reloj

    def consultar(self, bus_id: str, paradero_id: str) -> Seguimiento:
        lectura = self.repositorio.obtener(bus_id, paradero_id)
        if lectura is None:
            return Seguimiento(bus_id, paradero_id, None, None, "SIN_DATOS")
        ahora = self.reloj()
        if not lectura.vigente(ahora):
            return Seguimiento(bus_id, paradero_id, None,
                               ahora - lectura.capturada_s, "SIN_SEÑAL")
        return Seguimiento(bus_id, paradero_id, lectura.eta_min,
                           ahora - lectura.capturada_s, "ACTUAL")


class VistaSeguimiento:
    def __init__(self, consulta: ConsultaSeguimiento, mapas: Mapas):
        self.consulta, self.mapas = consulta, mapas

    def mostrar(self, bus_id: str, paradero_id: str) -> dict:
        resultado = self.consulta.consultar(bus_id, paradero_id)
        try:
            mapa = self.mapas.obtener()
        except (TimeoutError, ConnectionError):
            mapa = None
        return {
            "seguimiento": resultado,
            "mapa": mapa,
            "aviso": "Mapa no disponible; consulte el estado textual" if mapa is None else "",
        }
