# Prompt 03 — Escenarios de atributos de calidad

- **Fecha:** 29/09/2026
- **Herramienta:** Claude (asistente de IA)
- **Archivo hermano:** registrado en `bitacora-ia.md`, entrada 1 (decisión: **Corregida**)

## Prompt (texto exacto)

```text
Actúa como arquitecto de software. Contexto: RutaSIT Arequipa, 300 buses envían su
posición cada 10 s y el tiempo estimado de llegada (ETA) debe actualizarse en ≤ 15 s.
Tarea: redacta 3 escenarios de atributos de calidad en formato de seis partes
(fuente, estímulo, entorno, artefacto, respuesta, medida). El primero debe ser el
atributo crítico (rendimiento en tiempo real).

Regla: cada medida debe ser numérica y verificable; no uses palabras vagas como
"rápido", "seguro" o "fácil".
```

## Resumen de la respuesta de la IA

Tres escenarios correctos en estructura, pero con medidas vagas: «la aplicación debe responder
rápido» y «el sistema debe ser confiable».

## Verificación humana

Se sustituyeron todas las medidas por valores numéricos tomados del caso:

| Escenario | Medida original (vaga) | Medida corregida (numérica) |
|-----------|------------------------|------------------------------|
| QA-01 Rendimiento | «responder rápido» | p95 del ETA ≤ 15 s; 100 % de posiciones del minuto procesadas |
| QA-02 Disponibilidad | «ser confiable» | 0 pantallas vacías; recuperación ≤ 5 min |
| QA-03 Escalabilidad | «soportar más buses» | CPU < 70 % y p95 del ETA ≤ 15 s con 600 buses |

El resultado final está en `docs/architecture/drivers.md`, sección 4.
