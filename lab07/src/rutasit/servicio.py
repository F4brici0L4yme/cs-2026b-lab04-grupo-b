"""Versión con patrones del flujo consultar_seguimiento."""

from __future__ import annotations

from dataclasses import dataclass

from .estados import estado_desde_nombre
from .eta import FabricaETAs, FabricaGPS
from .eventos import NotificadorSMS, PanelOperador, PublicadorEventos
from .externos import ClienteLLMFalso
from .ia import AdaptadorLLMFalso, ConCache, cadena_guardrails


@dataclass
class Bus:
    id: str = "BUS-01"
    estado: str = "EN_ESPERA"
    edad_s: int = 5
    distancia_m: float = 10.0
    cerca_paradero: bool = False

    def cambiar_a(self, estado_obj):
        self.estado = estado_obj.nombre


@dataclass
class Paradero:
    id: str = "P-01"
    nombre: str = "San Camilo"


class ServicioSeguimiento:
    def __init__(self, gps_a=None, gps_b=None, llm=None):
        self.fabrica_gps = FabricaGPS(gps_a=gps_a, gps_b=gps_b)
        self.fabrica_eta = FabricaETAs()
        self.eventos: list = []
        self.publicador = PublicadorEventos()
        self.publicador.suscribir("seguimiento", NotificadorSMS(self.eventos))
        self.publicador.suscribir("seguimiento", PanelOperador(self.eventos))
        cliente = llm or ClienteLLMFalso()
        self.proveedor_llm = ConCache(AdaptadorLLMFalso(cliente))
        self.guardrails = cadena_guardrails()

    def consultar_seguimiento(self, bus, paradero_id, proveedor, algoritmo):
        gps = self.fabrica_gps.crear(proveedor)
        eta_strategy = self.fabrica_eta.crear(algoritmo)
        if bus.edad_s > 30:
            return bus.estado
        estado_obj = estado_desde_nombre(bus.estado)
        estado_obj.iniciar(bus)
        eta = eta_strategy.calcular(bus.distancia_m)
        ubicacion = gps.obtener_ubicacion(bus.id)
        if not ubicacion.ok:
            return bus.estado
        if bus.distancia_m > 30:
            bus.estado = "DESVIADO"
            mensaje = f"Desvío detectado ETA {eta}"
        elif bus.cerca_paradero:
            bus.estado = "EN_PARADERO"
            mensaje = f"Llegando a {paradero_id} ETA {eta}"
        else:
            bus.estado = "EN_RUTA"
            mensaje = "En ruta ETA {}".format(eta)
        self.publicador.publicar("seguimiento", {"bus_id": bus.id, "mensaje": mensaje, "eta": eta})
        return bus.estado

    def explicar_retraso(self, evento, proveedor_llm):
        if proveedor_llm not in ("FAKE", "OTRO"):
            raise ValueError(f"Proveedor LLM no soportado: {proveedor_llm}")
        texto = self.proveedor_llm.completar(evento)
        return self.guardrails.validar(texto)
