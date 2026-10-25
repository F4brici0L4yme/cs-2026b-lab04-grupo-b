"""Servicios externos simulados: GPS de dos operadores e LLM falso."""

from __future__ import annotations


class GpsOperadorA:
    """SDK simulado A: cobra en dict, responde con diccionario."""

    def __init__(self, fallas: int = 0):
        self.fallas = fallas
        self.llamadas = 0

    def realizar_lectura(self, bus_id: str) -> dict:
        self.llamadas += 1
        if self.fallas > 0:
            self.fallas -= 1
            raise TimeoutError("GPS A sin respuesta")
        if bus_id == "SIN_SENAL":
            return {"ok": False}
        return {"ok": True, "lat": -16.409, "lon": -71.537}


class GpsOperadorB:
    """SDK simulado B: interfaz distinta, responde con tupla (codigo, lat, lon)."""

    def __init__(self, fallas: int = 0):
        self.fallas = fallas
        self.llamadas = 0

    def fetch_position(self, bus_id: str) -> tuple:
        self.llamadas += 1
        if self.fallas > 0:
            self.fallas -= 1
            raise TimeoutError("GPS B timeout")
        if bus_id == "SIN_SENAL":
            return (404, None, None)
        return (200, -16.409, -71.537)


class ClienteLLMFalso:
    """LLM simulado: devuelve una respuesta fija, sin red ni API key."""

    def __init__(self, respuesta: str = "Retraso por congestión en Av. Ejército."):
        self.respuesta = respuesta
        self.llamadas = 0

    def completar(self, prompt: str) -> str:
        self.llamadas += 1
        return self.respuesta
