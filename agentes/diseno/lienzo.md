# Lienzo de diseño del sistema agéntico RutaSIT

| Decisión | Elección | Justificación |
|---|---|---|
| ¿Agente o flujo de trabajo? | Agente acotado ReAct para investigar y corregir; flujos fijos para ejecutar pruebas y producir métricas. | La localización de cada causa depende del código; la verificación debe ser determinista. |
| Arquetipo | Planificador-ejecutor con ciclo ReAct; actor-crítico de dos rondas para ISSUE-02. | El plan hace explícito el trabajo y el crítico puede detectar defectos de borde. |
| Herramientas | listar, leer, buscar, editar por coincidencia única, ejecutar pytest/radon de lista permitida, ver cambios y notas. | Solo se habilita lo imprescindible para inspeccionar y verificar. |
| Memoria | Historial corto por ejecución y archivo `agentes/notas.md`. | El historial conserva observaciones de la tarea; las notas permiten dejar una hipótesis útil al resolver ISSUE-03. |
| Coordinación | Gestor/planificador + ejecutor + revisor de solo lectura; máximo dos rondas. | El crítico no edita y el ciclo se limita para evitar una cadena indefinida. |
| Rol humano | El integrante revisa y aprueba o rechaza cada edición en modo `--aprobar-ediciones`; el humano conserva la integración. | La primera versión no debe fusionar cambios ni operar credenciales reales. |
| Control | Contrato JSON estricto, política por rol, sandbox, pruebas protegidas, allowlist de comandos, 12 pasos y máximo 2 rondas. | Reduce errores de formato, acciones fuera de alcance y bucles. |

## Caso de estudio

RutaSIT Arequipa: tres issues sembrados en un módulo demostrativo aislado de
los entregables Lab05–08. Las pruebas de `tests/` son la definición objetiva de
resuelto y nunca se editan desde la política del agente.
