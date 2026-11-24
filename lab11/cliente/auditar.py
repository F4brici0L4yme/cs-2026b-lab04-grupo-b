"""Auditor simple del catálogo MCP antes de conectarlo a un host."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from mcp.client import Client

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
from servidor_mcp.rutasit_mcp import mcp

PATRONES = ("ignora instrucciones", "secreto", "credencial", "contraseña", "api key")

async def auditar(cliente: Client) -> int:
        herramientas = (await cliente.list_tools()).tools
        problemas = 0
        for herramienta in herramientas:
            descripcion = (herramienta.description or "").lower()
            hallazgos = [p for p in PATRONES if p in descripcion]
            if not herramienta.annotations:
                hallazgos.append("sin anotaciones")
            if not (herramienta.annotations and herramienta.annotations.read_only_hint) and herramienta.annotations.destructive_hint is None:
                hallazgos.append("escritura sin destructiveHint")
            if "descripcion" in herramienta.input_schema.get("properties", {}) and "maxLength" not in str(herramienta.input_schema):
                hallazgos.append("texto libre sin límite de esquema")
            print(f"[{'OK' if not hallazgos else 'REVISAR'}] {herramienta.name}: {', '.join(hallazgos) or 'sin hallazgos'}")
            problemas += bool(hallazgos)
        return problemas


async def main() -> None:
    async with Client(mcp, mode="2026-07-28", read_timeout_seconds=5) as cliente:
        await auditar(cliente)

if __name__ == "__main__":
    asyncio.run(main())
