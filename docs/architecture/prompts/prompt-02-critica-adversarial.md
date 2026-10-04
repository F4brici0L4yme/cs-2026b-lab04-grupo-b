# Prompt 02 — Crítica adversarial ("abogado del diablo")

- **Fecha:** 30/09/2026
- **Herramienta:** Claude (asistente de IA)
- **Archivo hermano:** registrado en `bitacora-ia.md`, entrada 3 (decisión: **Corregida**)

## Prompt (texto exacto)

```text
Ahora actúa como "abogado del diablo". Critica duramente la alternativa que recomendaste
para RutaSIT Arequipa: ¿qué supuestos no se cumplen con nuestras restricciones (1 mes,
3 developers, un VPS)?, ¿qué podría fallar en producción con 300 buses enviando posición
cada 10 s?, ¿qué costo oculto tiene?

Enumera los 5 riesgos más graves y, para cada uno, una táctica arquitectónica de mitigación
concreta. No propongas tecnologías inexistentes ni capacidades que no estén documentadas.
```

## Resumen de la respuesta de la IA (5 riesgos)

1. Pérdida de eventos en picos de concurrencia → cola con reintentos.
2. Crecimiento ilimitado de la memoria de la cola → límite de tamaño y descarte por antigüedad.
3. Acoplamiento entre módulos del monolito → fronteras por interfaces y `import-linter` en CI.
4. ETA sesgado por imprecisión del GPS → suavizado (media móvil) y descarte de saltos.
5. Caída del VPS único → respaldo y reinicio automático, monitoreo.
Sugerencia adicional: usar una base de datos de series temporales (InfluxDB).

## Verificación humana

- Se aceptaron las tácticas de **cola con reintentos idempotentes** y de **mostrar la última
  posición conocida** (esta última se convirtió en el escenario QA-02).
- Se **descartó InfluxDB** por costo y curva de aprendizaje, contrarios a R-02 y R-03; para el
  MVP basta PostgreSQL en el mismo VPS.
- El equipo mantuvo la decisión C de la matriz; la crítica no cambió el estilo elegido, pero sí
  las tácticas de mitigación.
