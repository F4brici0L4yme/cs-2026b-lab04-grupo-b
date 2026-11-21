"""Resume métricas observables de trazas JSONL sin inferir datos externos."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def medir_trazas(rutas: Iterable[Path]) -> dict[str, object]:
    eventos = []
    rondas = set()
    for ruta in rutas:
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            if not linea.strip():
                continue
            evento = json.loads(linea)
            eventos.append(evento)
            agente = str(evento.get("agente", ""))
            if "_r" in agente:
                rondas.add(agente.rsplit("_r", 1)[1])
            elif evento.get("estado") == "FINALIZADO":
                rondas.add("1")
    herramientas = sorted({str(e["accion"]) for e in eventos if e.get("accion")})
    finales = [e for e in eventos if e.get("estado") == "FINALIZADO"]
    return {
        "pasos": len(eventos),
        "rondas": len(rondas),
        "herramientas": herramientas,
        "decisiones_rechazadas_contrato": sum(
            e.get("estado") == "CONTRATO_INVALIDO" for e in eventos
        ),
        "acciones_bloqueadas": sum(
            bool(e.get("bloqueada")) and bool(e.get("accion")) for e in eventos
        ),
        "acciones": sum(bool(e.get("accion")) for e in eventos),
        "contexto_final_caracteres": sum(
            int(e.get("contexto_caracteres", 0)) for e in finales
        ),
    }


def linea_markdown(nombre: str, metricas: dict[str, object]) -> str:
    herramientas = ", ".join(metricas["herramientas"]) or "ninguna"
    return (
        f"| {nombre} | {metricas['pasos']} | {metricas['rondas']} | "
        f"{herramientas} | {metricas['decisiones_rechazadas_contrato']} | "
        f"{metricas['acciones_bloqueadas']} | "
        f"{metricas['contexto_final_caracteres']} |"
    )
