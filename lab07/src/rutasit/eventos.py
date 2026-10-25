"""Observer de notificaciones: SMS y panel sin acoplarse al servicio."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Suscriptor(ABC):
    @abstractmethod
    def actualizar(self, evento: str, datos: dict): ...


class PublicadorEventos:
    def __init__(self):
        self._suscriptores: dict = {}

    def suscribir(self, evento: str, suscriptor: Suscriptor):
        self._suscriptores.setdefault(evento, []).append(suscriptor)

    def publicar(self, evento: str, datos: dict):
        for s in self._suscriptores.get(evento, []):
            s.actualizar(evento, datos)


class NotificadorSMS(Suscriptor):
    def __init__(self, bandeja: list):
        self._bandeja = bandeja

    def actualizar(self, evento, datos):
        self._bandeja.append(f"sms:{datos['bus_id']}:{datos['mensaje']}")


class PanelOperador(Suscriptor):
    def __init__(self, bandeja: list):
        self._bandeja = bandeja

    def actualizar(self, evento, datos):
        self._bandeja.append(f"panel:{datos['bus_id']}:{datos['eta']:.2f}")
