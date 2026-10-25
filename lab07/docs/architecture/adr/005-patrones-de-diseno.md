# ADR-005: Patrones de diseño en RutaSIT

- **Estado:** Aceptado (25/10/2026)
- **Decisores:** Grupo B (Layme, Auccacusi, Castillo)

## Contexto

`consultar_seguimiento()` tenía complejidad C(18); cada GPS o algoritmo obligaba a modificar el servicio. La salida del LLM no es confiable (inventa precios).

## Decisión

Adapter + Strategy + Factory para GPS/ETA; Decorator para reintentos y caché; State para Bus (Lab 05); Observer para SMS/panel; Chain of Responsibility para guardrails IA. Se rechazan Singleton y Abstract Factory (ver bitácora, entrada 1).

## Consecuencias

(+) Complejidad máxima 5, promedio 1.69; nuevos GPS/algoritmos sin modificar servicio; IA probable sin API. Pruebas: 30 passed, 1 xfailed.
(-) 239 SLOC frente a 89 y más indirección: el equipo debe conocer los patrones.
