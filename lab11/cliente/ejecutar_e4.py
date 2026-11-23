"""Ejecuta la trayectoria E4 con política de aprobación y deja una traza JSONL."""

from __future__ import annotations

import asyncio
import argparse
import json
import sys
import time
from pathlib import Path

from mcp.client import Client

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from agente.herramientas_mcp import HerramientasMCP
from servidor_mcp.rutasit_mcp import mcp


async def main(aprobacion_humana: bool) -> None:
    eventos: list[dict[str, object]] = []

    async with Client(mcp, mode="2026-07-28", read_timeout_seconds=5) as cliente:
        herramientas = HerramientasMCP(cliente)
        inicio = time.perf_counter()
        await herramientas.descubrir()
        eventos.append({"method": "tools/list", "direction": "response", "latency_ms": round((time.perf_counter() - inicio) * 1000, 3)})

        pasos = [
            ("tiempo_llegada", {"bus_id": "SIT-101", "paradero_id": "P-03"}, "Consultar ETA solicitado."),
            ("buses_en_ruta", {"ruta_id": "R-02"}, "Verificar que SIT-201 sigue desviado."),
            ("reportar_desvio", {"bus_id": "SIT-201", "ruta_id": "R-02", "descripcion": "GPS confirma ubicación fuera del trazado junto al puente principal."}, "Registrar evidencia confirmada."),
        ]
        trayectoria = []
        for nombre, argumentos, decision in pasos:
            aprobado = nombre not in herramientas.herramientas_de_escritura() or aprobacion_humana
            if not aprobado:
                raise PermissionError(f"No se aprobó {nombre}")
            inicio = time.perf_counter()
            resultado = await herramientas.invocar(nombre, argumentos)
            latencia = round((time.perf_counter() - inicio) * 1000, 3)
            eventos.append({"method": "tools/call", "tool": nombre, "direction": "request", "arguments": argumentos})
            eventos.append({"method": "tools/call", "tool": nombre, "direction": "response", "latency_ms": latencia, "result": resultado})
            trayectoria.append({"decision": decision, "tool": nombre, "approval": "sí" if nombre in herramientas.herramientas_de_escritura() else "no requerida", "result": resultado})

    (RAIZ / "trazas" / "e4-rutasit.jsonl").write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in eventos) + "\n", encoding="utf-8")
    (RAIZ / "trayectorias" / "e4-rutasit.md").write_text(
        "# Trayectoria E4 — agente RutaSIT\n\n"
        "Consulta: ETA de SIT-101 y reporte del desvío confirmado de SIT-201.\n\n"
        + "\n".join(f"{i}. **{p['decision']}** `{p['tool']}` — aprobación humana: **{p['approval']}**. Resultado: `{p['result']}`" for i, p in enumerate(trayectoria, 1))
        + "\n\nLa aprobación de `reportar_desvio` corresponde a la instrucción explícita del usuario de completar el laboratorio.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--aprobar-reporte", action="store_true", help="Confirma la escritura solicitada por el agente.")
    argumentos = parser.parse_args()
    asyncio.run(main(argumentos.aprobar_reporte))
