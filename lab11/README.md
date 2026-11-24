# Laboratorio 11 — Servidor MCP de RutaSIT Arequipa

RutaSIT publica consultas de buses y ETA para hosts compatibles con Model
Context Protocol (MCP) 2026-07-28. El transporte es `stdio` y no requiere red.
Para E5 se usa **Codex CLI como host MCP**, decisión confirmada por el equipo. La versión probada descubre herramientas y recursos, pero no invoca prompts MCP; esa limitación y la evidencia real están registradas en `uso-en-host.md`.

## Catálogo

| Capacidad | Tipo | Escritura |
|---|---|---:|
| `buses_en_ruta` | Herramienta | No |
| `tiempo_llegada` | Herramienta | No |
| `reportar_desvio` | Herramienta | Sí, crea un reporte nuevo |
| `rutasit://mapa/rutas`, `rutasit://reglas/operacion` | Recursos | No |
| `rutasit://adr/{numero}` | Recurso plantilla | No |
| `aviso_usuarios` | Prompt | No |

## Ejecutar y verificar

```bash
python -m pip install -e '.[dev]'
python cliente/explorar.py
python -m pytest -q
python cliente/auditar.py
```

El inspector se inicia con:

```bash
npx @modelcontextprotocol/inspector python servidor_mcp/rutasit_mcp.py
```

Para usar Codex CLI como host local:

```bash
codex mcp add rutasit -- python servidor_mcp/rutasit_mcp.py
codex mcp list
```

La configuración y las cinco consultas de host se registran en
[`uso-en-host.md`](uso-en-host.md). El diagrama y las métricas reproducibles
se generan con `python cliente/ejecutar_e4.py` y `python cliente/traza_mcp.py`.

## Estructura

El servidor, cliente, adaptador del agente, pruebas, traza, auditoría y
documentación viven íntegramente en `lab11/`, siguiendo la organización de los
laboratorios anteriores.
