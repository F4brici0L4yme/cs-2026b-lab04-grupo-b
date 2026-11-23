# E5 — Uso con host real: Codex CLI

Se eligió **Codex CLI** como host MCP porque admite servidores locales por
`stdio`; la guía acepta hosts compatibles y el equipo confirmó este uso.

## Conexión

```bash
cd lab11
codex mcp add rutasit -- .venv/bin/python servidor_mcp/rutasit_mcp.py
codex mcp list
```

Ejecutar una conversación nueva de Codex desde `lab11/` después de registrar el
servidor. Codex debe solicitar confirmación antes de `reportar_desvio`.

## Registro de cinco consultas (ejecución observada el 23/11/2026)

| Consulta | Herramienta o prompt esperado | Permiso | Resultado real |
|---|---|---|---|
| ¿Qué buses están activos en R-01? | `buses_en_ruta` | No | Codex invocó la herramienta; devolvió SIT-101 (EN_RUTA, P-03) y SIT-102 (EN_PARADERO, P-02). |
| ¿Cuándo llega SIT-101 a P-03? | `tiempo_llegada` | No | Codex invocó la herramienta; devolvió ETA 4.5 min, estado `ACTUAL`. |
| Lee el mapa de rutas y dime los paraderos de R-02. | `resources/read` sobre `rutasit://mapa/rutas` | No | Codex leyó el recurso; devolvió P-07 y P-08. |
| Usa el prompt aviso a usuarios para R-02 con estado DESVIADO. | `aviso_usuarios` | No | **No completada por el host:** Codex CLI listó recursos/plantillas pero informó que el prompt no estaba expuesto en esa sesión. El servidor sí lo publica y el cliente oficial lo verifica en la prueba de contrato. |
| Reporta el desvío confirmado de SIT-201 en R-02. | `reportar_desvio` | Sí, autorización explícita del usuario | Codex invocó la herramienta y creó `reportes/DESVIO-03.md`; contenido y evidencia validados. |

Los resultados corresponden a dos sesiones reales de `codex exec`. La cuarta fila documenta una incompatibilidad de este host/versionado con prompts MCP; no se reemplaza por una salida simulada. Para cumplir esa capacidad con host real, se requiere repetir solo esa fila en VS Code Copilot, Claude Code o Gemini CLI.
