"""Composition root: único lugar de producción que conecta adaptadores."""

from rutasit8.aplicacion.seguimiento import ConsultaSeguimiento, VistaSeguimiento
from rutasit8.infraestructura.cache import ConCacheETA
from rutasit8.infraestructura.resiliencia import ConCircuitBreaker


def construir(repositorio, mapas, reloj) -> VistaSeguimiento:
    consulta = ConsultaSeguimiento(ConCacheETA(repositorio, reloj), reloj)
    return VistaSeguimiento(consulta, ConCircuitBreaker(mapas, reloj))
