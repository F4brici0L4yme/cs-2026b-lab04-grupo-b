"""Mini framework acotado para agentes de código reproducibles."""

from .contrato import validar_decision
from .nucleo import Agente
from .politica import Decision, Politica

__all__ = ["Agente", "Decision", "Politica", "validar_decision"]
