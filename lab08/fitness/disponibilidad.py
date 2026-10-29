"""Falla de mapas durante 20 min; ejecuta el breaker y la vista reales del prototipo."""

from rutasit8.aplicacion.seguimiento import ConsultaSeguimiento, VistaSeguimiento
from rutasit8.dominio import LecturaETA
from rutasit8.infraestructura.memoria import RepositorioMemoria
from rutasit8.infraestructura.resiliencia import ConCircuitBreaker


class Reloj:
    ahora = 0.0

    def __call__(self):
        return self.ahora


class MapasSimulados:
    def __init__(self, reloj, inicio=300, fin=1500):
        self.reloj, self.inicio, self.fin = reloj, inicio, fin
        self.llamadas_en_caida = 0

    def obtener(self):
        if self.inicio <= self.reloj() < self.fin:
            self.llamadas_en_caida += 1
            raise TimeoutError("Caída inyectada de mapas")
        return "tile-simulado"


def simular(modo="breaker", espera_s=30):
    reloj = Reloj()
    proveedor, repo = MapasSimulados(reloj), RepositorioMemoria()
    consulta = ConsultaSeguimiento(repo, reloj)
    mapas = ConCircuitBreaker(proveedor, reloj, espera_s=espera_s) if modo == "breaker" else proveedor
    vista = VistaSeguimiento(consulta, mapas)
    vacias, degradadas, primera_recuperacion = 0, 0, None
    for t in range(1800):
        reloj.ahora = float(t)
        if t % 10 == 0:
            repo.guardar(LecturaETA("BUS-01", "P-01", t, t, 3.0))
        if modo == "base":
            try:
                proveedor.obtener()
            except TimeoutError:
                vacias += 1
                continue
            tiene_mapa = True
        elif modo == "reintentos":
            tiene_mapa = False
            for _ in range(3):
                try:
                    proveedor.obtener()
                    tiene_mapa = True
                    break
                except TimeoutError:
                    pass
            if not tiene_mapa:
                vacias += 1
        else:
            respuesta = vista.mostrar("BUS-01", "P-01")
            tiene_mapa = respuesta["mapa"] is not None
            degradadas += not tiene_mapa
            vacias += respuesta["seguimiento"] is None
        if t >= 1500 and tiene_mapa and primera_recuperacion is None:
            primera_recuperacion = t - 1500
    return {"consultas": 1800, "pantallas_vacias": vacias, "degradadas": degradadas,
            "llamadas_en_caida": proveedor.llamadas_en_caida,
            "recuperacion_s": primera_recuperacion}
