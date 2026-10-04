# Prompt 04 — Matriz de decisión, pesos y gráfico

- **Fecha:** 30/09/2026
- **Herramienta:** Claude (asistente de IA)
- **Archivo hermano:** registrado en `bitacora-ia.md`, entrada 5 (decisión: **Corregida**)

## Prompt (texto exacto)

```text
Actúa como arquitecto de software. Con estos drivers (atributo crítico: rendimiento
en tiempo real, QA-01; plazo de 1 mes, R-01; presupuesto de un VPS, R-03; equipo de
3 developers, R-02), propón 5 criterios con pesos que sumen exactamente 100 %,
justifica cada peso citando su driver y genera un script de matplotlib que dibuje el
total ponderado de las 3 alternativas.
```

## Resumen de la respuesta de la IA

Propuesta de criterios con pesos 30 + 25 + 20 + 15 + 15 = **105 %** y un script de matplotlib
que dibuja el total ponderado en barras horizontales.

## Verificación humana

- Se detectó que los pesos **no sumaban 100 %**. Se ajustó *Modificabilidad* de 15 % a 10 %,
  quedando 30 + 25 + 20 + 15 + 10 = 100 %.
- Se recalculó cada total ponderado a mano antes de aceptar la figura.
- El script aceptado y versionado vive en `docs/architecture/diagramas/matriz_decision.py`.
