"""State del bus: implementa la máquina de estados del Lab 05."""

from __future__ import annotations


class EstadoBus:
    nombre = "?"

    def iniciar(self, bus):
        raise ValueError("Estado no válido para iniciar seguimiento")

    def marcar_desvio(self, bus):
        raise ValueError(f"No se puede marcar desvío desde {self.nombre}")

    def marcar_en_ruta(self, bus):
        raise ValueError(f"No se puede marcar en ruta desde {self.nombre}")

    def marcar_en_paradero(self, bus):
        raise ValueError(f"No se puede marcar en paradero desde {self.nombre}")


class EnEspera(EstadoBus):
    nombre = "EN_ESPERA"

    def iniciar(self, bus):
        bus.cambiar_a(EnRuta())


class EnRuta(EstadoBus):
    nombre = "EN_RUTA"

    def marcar_desvio(self, bus):
        bus.cambiar_a(Desviado())

    def marcar_en_ruta(self, bus):
        bus.cambiar_a(EnRuta())

    def marcar_en_paradero(self, bus):
        bus.cambiar_a(EnParadero())


class EnParadero(EstadoBus):
    nombre = "EN_PARADERO"

    def marcar_en_ruta(self, bus):
        bus.cambiar_a(EnRuta())

    def marcar_desvio(self, bus):
        bus.cambiar_a(Desviado())


class Desviado(EstadoBus):
    nombre = "DESVIADO"

    def iniciar(self, bus):
        raise ValueError("Bus desviado, requiere operador")


class FueraDeServicio(EstadoBus):
    nombre = "FUERA_DE_SERVICIO"

    def iniciar(self, bus):
        raise ValueError("Bus fuera de servicio")


_ESTADOS = {
    "EN_ESPERA": EnEspera,
    "EN_RUTA": EnRuta,
    "EN_PARADERO": EnParadero,
    "DESVIADO": Desviado,
    "FUERA_DE_SERVICIO": FueraDeServicio,
}


def estado_desde_nombre(nombre: str) -> EstadoBus:
    if nombre not in _ESTADOS:
        raise ValueError("Estado no válido para iniciar seguimiento")
    return _ESTADOS[nombre]()
