# ADR-010: sistema agéntico acotado para RutaSIT

## Estado

Propuesto para revisión humana. No aprobado ni integrado.

## Decisores

Grupo B — RutaSIT Arequipa.

## Contexto

El repositorio contiene el caso RutaSIT y entregables de Labs 05–08. Se
requieren agentes capaces de explorar y corregir tres incidencias, con pruebas
objetivas, sin credenciales de API y sin editar sus propias pruebas. El trabajo
debe ejecutarse en sandbox/ramas de trabajo; el agente no debe fusionar su
cambio.

## Alternativas consideradas

1. **Flujo fijo de scripts:** fácil de auditar, pero no puede decidir qué
   archivo inspeccionar ante causas distintas.
2. **Agente único sin límites:** reduce implementación inicial, pero permite
   llamadas de herramienta arbitrarias, ediciones de pruebas y bucles.
3. **Sistema propuesto, planificador-ejecutor con ReAct y crítico de solo
   lectura:** mantiene flexibilidad de exploración, añade política y revisión,
   con costo acotado por pasos y rondas.

## Decisión

Construir un mini framework Python de aproximadamente 300 líneas, con contrato
JSON estricto, `ModeloInteractivo` y `ModeloGrabado`, herramientas de lectura,
búsqueda, mapa AST, edición exacta, pruebas permitidas, notas y trazas JSONL.
El ejecutor solo puede editar el módulo demostrativo de `lab09`; `tests/`,
`issues/`, red, merge y publicación quedan fuera de sus permisos.

Para ISSUE-02 se comparan agente único y actor-crítico con máximo dos rondas.
El revisor no edita. La política puede preguntar aprobación `s`/`n` antes de
cada edición; no reemplaza la revisión cruzada del PR por un integrante.

## Consecuencias

- Positivas: trayectoria reproducible sin API; pruebas previas y posteriores;
  bloqueos por rol; límites explícitos; revisión del caso degenerado de la ruta.
- Negativas: el modelo grabado no mide variabilidad de un proveedor real; el
  prototipo no es un sistema de producción y no ejecuta sobre credenciales o
  código de producción.
- Pendientes: revisión del grupo, aprobación humana de ediciones/PR, ejecución
  manual interactiva por integrantes y etiqueta `v1.0-agentes`.
