# Prompt 08 — Render de los PNG

Origen: **fila #6** de [`../bitacora-ia.md`](../bitacora-ia.md); textos copiados sin cambios.

- **Fecha:** 17/10/2026
- **Herramienta:** OpenCode (asistente IA) + PlantUML

## Texto del prompt

> «Genera los PNG de las cinco vistas exportadas y del contexto manual».

## Propuesta de la IA (resumen)

Un solo comando con salida `-o ../img` para todos los `.puml`.

## Qué se corrigió por criterio humano

El PNG del contexto manual quedó en `docs/architecture/img/`: la ruta `../img` es relativa a cada archivo de entrada.

## Decisión tomada

Corregir la salida (`-o img`), mover el archivo y regenerar; error propio de la IA, registrado aquí.
