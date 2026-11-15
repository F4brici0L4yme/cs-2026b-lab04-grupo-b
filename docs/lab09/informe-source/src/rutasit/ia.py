"""IA aislada: Strategy + Adapter + Decorator (caché) + Chain (guardrails)."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ProveedorLLM(ABC):
    @abstractmethod
    def completar(self, prompt: str) -> str: ...


class AdaptadorLLMFalso(ProveedorLLM):
    """Adapter del LLM simulado."""

    def __init__(self, cliente):
        self._cliente = cliente

    def completar(self, prompt):
        return self._cliente.completar(prompt)


class ConCache(ProveedorLLM):
    """Decorator: evita pagar dos veces por el mismo prompt."""

    def __init__(self, interno: ProveedorLLM):
        self._interno, self._cache = interno, {}

    def completar(self, prompt):
        if prompt not in self._cache:
            self._cache[prompt] = self._interno.completar(prompt)
        return self._cache[prompt]


class Guardrail(ABC):
    def __init__(self, siguiente=None):
        self._siguiente = siguiente

    def validar(self, texto: str) -> str:
        texto = self._aplicar(texto)
        return self._siguiente.validar(texto) if self._siguiente else texto

    @abstractmethod
    def _aplicar(self, texto: str) -> str: ...


class SinPrecios(Guardrail):
    def _aplicar(self, texto):
        if "S/" in texto:
            raise ValueError("Guardrail: la IA incluyó un precio")
        return texto


class SinAfirmacionesProhibidas(Guardrail):
    PROHIBIDAS = ["diagnóstico", "cura", "garantizado"]

    def _aplicar(self, texto):
        for palabra in self.PROHIBIDAS:
            if palabra in texto.lower():
                raise ValueError(f"Guardrail: afirmación no permitida '{palabra}'")
        return texto


class LongitudMaxima(Guardrail):
    def _aplicar(self, texto):
        if len(texto) > 200:
            raise ValueError("Guardrail: respuesta demasiado larga")
        return texto


def cadena_guardrails() -> Guardrail:
    return SinPrecios(SinAfirmacionesProhibidas(LongitudMaxima()))
