"""Validación estricta del protocolo JSON usado por el agente."""

from __future__ import annotations

from collections.abc import Iterable


def validar_decision(
    decision: object,
    herramientas_conocidas: Iterable[str],
) -> tuple[bool, str]:
    if not isinstance(decision, dict):
        return False, "la decisión debe ser un objeto JSON"
    if not isinstance(decision.get("pensamiento"), str) or not decision["pensamiento"].strip():
        return False, "falta 'pensamiento' (texto no vacío)"
    tiene_accion = "accion" in decision
    tiene_final = "final" in decision
    if tiene_accion == tiene_final:
        return False, "debe incluir 'accion' o 'final', pero no ambos"
    if tiene_final:
        if set(decision) != {"pensamiento", "final"}:
            return False, "campos no permitidos en una decisión final"
        if not isinstance(decision["final"], str) or not decision["final"].strip():
            return False, "'final' debe ser texto no vacío"
        return True, ""
    if set(decision) - {"pensamiento", "accion", "args"}:
        return False, f"campos no permitidos: {sorted(set(decision) - {'pensamiento', 'accion', 'args'})}"
    accion = decision.get("accion")
    if not isinstance(accion, str) or not accion.strip():
        return False, "'accion' debe ser texto no vacío"
    if accion not in set(herramientas_conocidas):
        return False, f"herramienta desconocida: {accion!r}"
    if "args" in decision and not isinstance(decision["args"], dict):
        return False, "'args' debe ser un objeto JSON"
    return True, ""
