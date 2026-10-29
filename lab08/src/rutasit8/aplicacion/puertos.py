"""Inversión de dependencias heredada de los Labs 05–07."""

from typing import Protocol

from rutasit8.dominio import LecturaETA


class RepositorioETA(Protocol):
    def obtener(self, bus_id: str, paradero_id: str) -> LecturaETA | None: ...


class Mapas(Protocol):
    def obtener(self) -> str: ...
