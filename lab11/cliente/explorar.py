"""Explora el servidor en proceso con el cliente oficial MCP."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from mcp.client import Client

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
from servidor_mcp.rutasit_mcp import mcp


async def main() -> None:
    async with Client(mcp, mode="2026-07-28") as cliente:
        info = cliente.server_info
        print(f"Servidor: {info.name if info else 'RutaSIT'} | protocolo {cliente.protocol_version}")
        print("\nHERRAMIENTAS:")
        for herramienta in (await cliente.list_tools()).tools:
            modo = "ESCRITURA" if not herramienta.annotations.read_only_hint else "solo lectura"
            print(f"  - {herramienta.name} [{modo}]")
        print("\nRECURSOS:")
        for recurso in (await cliente.list_resources()).resources:
            print(f"  - {recurso.uri} {recurso.name}")
        for plantilla in (await cliente.list_resource_templates()).resource_templates:
            print(f"  - {plantilla.uri_template} {plantilla.name} (plantilla)")
        print("\nPROMPTS:")
        for prompt in (await cliente.list_prompts()).prompts:
            print(f"  - {prompt.name}")
        llegada = await cliente.call_tool("tiempo_llegada", {"bus_id": "SIT-101", "paradero_id": "P-03"})
        print("\nPRUEBA tiempo_llegada:", json.dumps(llegada.structured_content, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
