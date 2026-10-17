# Prompt 02 — Auditoría C4 de las vistas exportadas

Origen: **fila #7** de [`../bitacora-ia.md`](../bitacora-ia.md); textos copiados sin cambios.

- **Fecha:** 17/10/2026
- **Herramienta:** OpenCode (subagente revisor, Prompt IA 2 de la guía: «Auditor C4»)

## Texto del prompt

> «Evalúa las vistas exportadas con la lista de c4model.com (general, elementos, relaciones); responde en tabla con evidencia y corrección; no inventes problemas».

## Propuesta de la IA (resumen)

11 observaciones y 3 casos dudosos: externos sin gris, acrónimos, alcance del título, duplicación del `.puml`, paso 4 del flujo, falta de cliente, etc.

## Qué se corrigió por criterio humano

El equipo contrastó cada hallazgo con `workspace.dsl` y las fuentes: 2 correctos corregidos (acrónimos ETA/SIT/VPS; alcance del título de la dinámica), 2 falsos positivos confirmados por el equipo (duplicación del `.puml`; paso 4 resuelto por el patrón puertos/adaptadores), 1 limitación aceptada (gris de externos en `plantuml/c4plantuml`), 1 decisión de alcance (sin aplicación cliente) y 1 duda resuelta (la duplicación la genera el exportador).

## Decisión tomada

Corregir el modelo, re-exportar y registrar la matriz completa en `revision-c4.md`.
