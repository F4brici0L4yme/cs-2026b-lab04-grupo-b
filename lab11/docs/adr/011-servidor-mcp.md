# ADR-011: Exponer RutaSIT mediante MCP

## Contexto

El agente del proyecto necesita consultar buses y ETA sin incrustar esas funciones en cada host.

## Decisión

Se expone un servidor MCP 2026-07-28 por `stdio`, con dos consultas, un reporte de desvío que solo crea archivos, recursos de mapa/reglas/ADR y un prompt de aviso. Codex CLI es el host usado para la integración.

## Consecuencias

Los hosts descubren el catálogo dinámicamente. Las entradas se validan, el reporte exige aprobación humana y el catálogo se audita antes de conectarse. Se descartan REST directa, que obliga a cada agente a implementar un cliente propio, y function calling interno, que acopla las herramientas a un solo agente.
