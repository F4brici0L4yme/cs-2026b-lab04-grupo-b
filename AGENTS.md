# AGENTS.md — RutaSIT (Lab 12)

## Contexto
Proyecto Python por laboratorios. RutaSIT Arequipa modela seguimiento de buses. La historia HU-12 mejora la ETA usando la distancia restante sobre el trazado de ruta. Lee `specs/hu-12/spec.md`, `plan.md` y `tasks.md` antes de modificar código.

## Forma de trabajo
1. Una tarea a la vez: prueba observable primero, código mínimo después.
2. Reutiliza `lab05/src/rutasit` y conserva sus contratos; Lab 10 ya cubre ETA no negativa, segmento degenerado y GPS sin datos.
3. No edites pruebas para que pasen ni dependencias no aprobadas. Explica los cambios y las verificaciones.
4. No inventes métricas ni ejecuciones, revisiones, decisiones humanas o resultados de CI.

## Compuertas
Ejecuta `python calidad/verificar.py hu-12`: pruebas focalizadas, cobertura >=85% del módulo HU-12, Ruff, Bandit, Radon (máximo B), dependencias aprobadas y regresiones seleccionadas de Labs 05, 07 y 10. CI debe ejecutar la misma verificación.

## Seguridad
Solo datos ficticios. Nunca incluyas secretos, datos personales, shell arbitraria, `eval`, `exec` o `pickle` externo en prompts o código. Revisa dependencias antes de usarlas.
