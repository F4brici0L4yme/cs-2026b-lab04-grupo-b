"""Adaptador MCP para que el agente del Lab 10 descubra RutaSIT dinámicamente."""

from __future__ import annotations

from mcp.client import Client


class HerramientasMCP:
    def __init__(self, cliente: Client) -> None:
        self.cliente = cliente
        self._herramientas = {}

    async def descubrir(self) -> None:
        self._herramientas = {herramienta.name: herramienta for herramienta in (await self.cliente.list_tools()).tools}

    def catalogo(self) -> dict[str, str]:
        return {nombre: herramienta.description or "" for nombre, herramienta in self._herramientas.items()}

    def herramientas_de_escritura(self) -> set[str]:
        return {nombre for nombre, herramienta in self._herramientas.items() if not herramienta.annotations.read_only_hint}

    async def invocar(self, nombre: str, argumentos: dict[str, object]) -> object:
        if nombre not in self._herramientas:
            return f"ERROR: herramienta desconocida: {nombre}"
        resultado = await self.cliente.call_tool(nombre, argumentos)
        if resultado.is_error:
            texto = " ".join(getattr(bloque, "text", "") for bloque in resultado.content)
            return f"ERROR: {texto}"
        return resultado.structured_content if resultado.structured_content is not None else " ".join(
            getattr(bloque, "text", "") for bloque in resultado.content
        )

    async def leer_recurso(self, uri: str) -> str:
        resultado = await self.cliente.read_resource(uri)
        return "\n".join(getattr(contenido, "text", "") for contenido in resultado.contents)
