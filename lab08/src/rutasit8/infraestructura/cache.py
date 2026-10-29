"""Decorator de lectura con TTL corto y tamaño limitado (ADR-007)."""

from collections import OrderedDict

from rutasit8.aplicacion.puertos import RepositorioETA
from rutasit8.dominio import LecturaETA


class ConCacheETA:
    def __init__(self, interno: RepositorioETA, reloj, ttl_s: float = 2,
                 capacidad: int = 2400):
        if not 0 < ttl_s <= 2 or capacidad < 1:
            raise ValueError("TTL debe ser (0, 2] y capacidad positiva")
        self.interno, self.reloj = interno, reloj
        self.ttl_s, self.capacidad = ttl_s, capacidad
        self.cache: OrderedDict[tuple[str, str], tuple[float, LecturaETA]] = OrderedDict()

    def obtener(self, bus_id: str, paradero_id: str) -> LecturaETA | None:
        clave, ahora = (bus_id, paradero_id), self.reloj()
        if clave in self.cache:
            expira, lectura = self.cache[clave]
            if ahora < expira and lectura.vigente(ahora):
                self.cache.move_to_end(clave)
                return lectura
            del self.cache[clave]
        lectura = self.interno.obtener(bus_id, paradero_id)
        if lectura is not None and lectura.vigente(ahora):
            self.cache[clave] = (ahora + self.ttl_s, lectura)
            if len(self.cache) > self.capacidad:
                self.cache.popitem(last=False)
        return lectura
