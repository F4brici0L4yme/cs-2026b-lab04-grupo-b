# ADR-012: Uso de IA en el desarrollo

- Estado: Propuesto para revisión del grupo
- Contexto: Lab 12 evalúa el desarrollo asistido por IA con pruebas, compuertas y supervisión humana.

## Decisión

- Herramienta permitida: asistente de programación en modo agente con contexto del repositorio. El equipo registra el nombre real de la herramienta y su modo al completar el PR.
- Se puede delegar borradores, pruebas propuestas, documentación y cambios acotados bajo spec y tareas. El equipo conserva diseño, revisión de cambios, aceptación de riesgos y aprobación de merge.
- No se delega aprobación final, publicación sin revisión, gestión de secretos ni decisiones de licencias/datos.
- Cada cambio debe pasar pytest y cobertura >=85 %, Ruff, Bandit, Radon máximo B, dependencias aprobadas y regresiones relevantes en CI.
- Commits/PR describen asistencia de IA cuando corresponda. Ningún miembro aprueba su propio PR.
- No se ingresan claves, tokens, datos personales ni código de terceros sin licencia compatible en prompts o artefactos.

## Consecuencias
La persona autora y el equipo que integra conservan responsabilidad por el código, incluida cualquier vulnerabilidad generada con IA. La herramienta no reemplaza revisión ni compuertas.

## Revisión
Pendiente de ratificación por el grupo.
