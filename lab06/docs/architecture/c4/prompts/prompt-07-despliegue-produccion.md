# Prompt 07 — Entorno de despliegue «Producción»

Origen: **fila #5** de [`../bitacora-ia.md`](../bitacora-ia.md); textos copiados sin cambios.

- **Fecha:** 17/10/2026
- **Herramienta:** OpenCode (asistente IA) + Structurizr CLI (Docker)

## Texto del prompt

> «Agrega el entorno "Producción" con nodos anidados e instancias de todos los contenedores».

## Propuesta de la IA (resumen)

Nodos de dispositivo para el pasajero y el operador (vacíos), más el VPS con las instancias y el nodo de buses con el rastreador.

## Qué se corrigió por criterio humano

Prueba real de export: Structurizr descarta del diagrama los nodos sin instancias; los dispositivos no aparecían en el PNG.

## Decisión tomada

Retirarlos del modelo (ningún contenedor de RutaSIT se ejecuta allí); corregir `inventario.md` y registrarlo.
