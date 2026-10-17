# Prompt 01 — Borrador del inventario y `workspace.dsl`

Origen: **fila #1** de [`../bitacora-ia.md`](../bitacora-ia.md); textos copiados sin cambios.

- **Fecha:** 17/10/2026
- **Herramienta:** OpenCode (asistente IA)

## Texto del prompt

> «Modela el inventario C4 y el borrador de `workspace.dsl` desde el Lab 04/05, sin inventar elementos».

## Propuesta de la IA (resumen)

Contenedores con Nginx (proxy HTTPS) y Grafana (monitoreo), porque aparecen en `despliegue.py` y QA-02.

## Qué se corrigió por criterio humano

El ADR-001 describe monolito modular + cola Redis + PostgreSQL; ni el proxy ni el monitoreo son contenedores del sistema y QA-02 no exige modelarlos en C4.

## Decisión tomada

Excluirlos de las vistas del MVP (decisión documentada); contenedores finales: API RutaSIT, Worker ETA/Alertas, Cola y caché y Base de datos.
