"""Versión ingenua del flujo consultar_seguimiento (se conserva para comparar)."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..externos import ClienteLLMFalso, GpsOperadorA, GpsOperadorB


@dataclass
class Bus:
    id: str = "BUS-01"
    estado: str = "EN_ESPERA"
    edad_s: int = 5
    distancia_m: float = 10.0
    cerca_paradero: bool = False


@dataclass
class Paradero:
    id: str = "P-01"
    nombre: str = "San Camilo"


class ServicioSeguimiento:
    def __init__(self, gps_a=None, gps_b=None, llm=None):
        self.gps_a = gps_a or GpsOperadorA()
        self.gps_b = gps_b or GpsOperadorB()
        self.llm = llm or ClienteLLMFalso()
        self.eventos: list = []

    def consultar_seguimiento(self, bus, paradero_id, proveedor, algoritmo):
        if bus.estado != "EN_ESPERA":
            if bus.estado == "FUERA_DE_SERVICIO":
                raise ValueError("Bus fuera de servicio")
            elif bus.estado == "DESVIADO":
                raise ValueError("Bus desviado, requiere operador")
            else:
                raise ValueError("Estado no válido para iniciar seguimiento")
        if bus.edad_s > 30:
            return bus.estado
        eta = 0.0
        if algoritmo == "BASE":
            eta = round(bus.distancia_m / 8.33 / 60, 2)
        elif algoritmo == "PUNTA":
            eta = round(bus.distancia_m / 4.16 / 60, 2)
        else:
            raise ValueError(f"Algoritmo no soportado: {algoritmo}")
        bus.estado = "EN_RUTA"
        ok, lat, lon = False, None, None
        if proveedor == "A":
            for intento in range(3):
                try:
                    r = self.gps_a.realizar_lectura(bus.id)
                    ok, lat, lon = r["ok"], r.get("lat"), r.get("lon")
                    break
                except TimeoutError:
                    if intento == 2:
                        ok = False
        elif proveedor == "B":
            for intento in range(3):
                try:
                    codigo, la, lo = self.gps_b.fetch_position(bus.id)
                    ok, lat, lon = codigo == 200, la, lo
                    break
                except TimeoutError:
                    if intento == 2:
                        ok = False
        else:
            raise ValueError(f"Proveedor GPS no soportado: {proveedor}")
        if not ok:
            return bus.estado
        if bus.distancia_m > 30:
            bus.estado = "DESVIADO"
            self.eventos.append(f"sms:{bus.id}:Desvío detectado ETA {eta}")
            self.eventos.append(f"panel:{bus.id}:{eta:.2f}")
        elif bus.cerca_paradero:
            bus.estado = "EN_PARADERO"
            self.eventos.append(f"sms:{bus.id}:Llegando a {paradero_id} ETA {eta}")
            self.eventos.append(f"panel:{bus.id}:{eta:.2f}")
        else:
            bus.estado = "EN_RUTA"
            self.eventos.append(f"sms:{bus.id}:En ruta ETA {eta}")
            self.eventos.append(f"panel:{bus.id}:{eta:.2f}")
        return bus.estado

    def explicar_retraso(self, evento, proveedor_llm):
        if proveedor_llm == "FAKE":
            texto = self.llm.completar(evento)
        elif proveedor_llm == "OTRO":
            texto = self.llm.completar(evento)
        else:
            raise ValueError(f"Proveedor LLM no soportado: {proveedor_llm}")
        if "S/" in texto:
            raise ValueError("Guardrail: la IA incluyó un precio")
        for palabra in ["diagnóstico", "cura", "garantizado"]:
            if palabra in texto.lower():
                raise ValueError(f"Guardrail: afirmación no permitida '{palabra}'")
        if len(texto) > 200:
            raise ValueError("Guardrail: respuesta demasiado larga")
        return texto
