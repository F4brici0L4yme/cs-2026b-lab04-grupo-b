"""Borrador ilustrativo de un prompt vago; ignora la forma de la ruta."""
import math

def eta_minutos(distancia_m: float, velocidad_m_s: float) -> float:
    return math.ceil(distancia_m / velocidad_m_s / 60)
