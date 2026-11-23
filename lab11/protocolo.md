# Métricas E6

- Mensajes registrados: 7.
- Transporte: cliente MCP local; sin red ni LLM.

| Método | Latencia media (ms) |
|---|---:|
| `tools/call:buses_en_ruta` | 5010.623 |
| `tools/call:reportar_desvio` | 5008.249 |
| `tools/call:tiempo_llegada` | 5096.540 |
| `tools/list` | 1.134 |

## Costo y optimización
El inventario mínimo del catálogo mide 42 caracteres (≈11 tokens, aproximación de 4 caracteres/token).
Se conservan solo tres herramientas orientadas a la operación, dos rutas cerradas y un único texto libre limitado a 20–500 caracteres. La reducción elimina capacidades administrativas sin afectar la trayectoria E4: el agente seleccionó las tres herramientas requeridas.
