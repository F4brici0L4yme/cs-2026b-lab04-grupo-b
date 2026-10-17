# Prompt 06 — Vista dinámica del flujo HU-06

Origen: **fila #4** de [`../bitacora-ia.md`](../bitacora-ia.md); textos copiados sin cambios.

- **Fecha:** 17/10/2026
- **Herramienta:** OpenCode (asistente IA) + Structurizr CLI (Docker)

## Texto del prompt

> «Construye la vista dinámica del flujo HU-06 sobre relaciones existentes, integrando ingesta, desvío y operador».

## Propuesta de la IA (resumen)

Vista con alcance del sistema y 9 pasos entre componentes y contenedores.

## Qué se corrigió por criterio humano

`structurizr validate` falló: «Components can't be added to a dynamic view when the scope is a software system»; además, con `!identifiers hierarchical` las relaciones exigen rutas completas.

## Decisión tomada

Alcance = contenedor API (patrón de la guía) y relaciones persona/GPS → Presentación; vista validada y exportada.
