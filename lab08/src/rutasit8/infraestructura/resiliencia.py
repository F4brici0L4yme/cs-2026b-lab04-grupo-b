"""Circuit breaker secuencial para el puerto de mapas (ADR-008)."""

from rutasit8.aplicacion.puertos import Mapas


class CircuitoAbierto(ConnectionError):
    pass


class ConCircuitBreaker:
    def __init__(self, interno: Mapas, reloj, umbral: int = 3, espera_s: float = 30):
        if umbral < 1 or espera_s <= 0:
            raise ValueError("Umbral y espera deben ser positivos")
        self.interno, self.reloj = interno, reloj
        self.umbral, self.espera_s = umbral, espera_s
        self.fallas, self.abierto_desde = 0, None

    @property
    def estado(self) -> str:
        if self.abierto_desde is None:
            return "CERRADO"
        if self.reloj() - self.abierto_desde >= self.espera_s:
            return "SEMIABIERTO"
        return "ABIERTO"

    def obtener(self) -> str:
        if self.estado == "ABIERTO":
            raise CircuitoAbierto("Proveedor temporalmente aislado")
        try:
            resultado = self.interno.obtener()
        except (TimeoutError, ConnectionError):
            self.fallas += 1
            if self.fallas >= self.umbral:
                self.abierto_desde = self.reloj()
            raise
        self.fallas, self.abierto_desde = 0, None
        return resultado
