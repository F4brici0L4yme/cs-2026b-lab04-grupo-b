1. El autocompletado sugiere código mientras se escribe; el modo agente puede inspeccionar y cambiar varios archivos y ejecutar comandos; un agente en segundo plano recibe una tarea y devuelve un PR para revisión. En RutaSIT usaríamos autocompletado para cambios locales, modo agente para una HU acotada y agente en segundo plano para una corrección bien especificada que pase las compuertas.

2. Vibe coding acepta una salida por apariencia; ingeniería asistida define criterios, pruebas, contexto, compuertas y revisión. El primero puede servir para prototipos descartables sin datos sensibles.

3. `AGENTS.md` documenta arquitectura por laboratorios, reutilización del puerto ETA, flujo TDD, compuertas y restricciones de secretos/dependencias. La medición cualitativa de cambios en respuestas se documentará en la bitácora; no se atribuye una mejora no medida.

4. Las pruebas fijan el comportamiento antes de implementar. En HU-12, la ruta curva hace que la distancia por trazado supere la distancia directa y evita que el estimador use la cuerda entre bus y paradero.

5. Slopsquatting consiste en registrar paquetes inexistentes sugeridos por un modelo para distribuir código malicioso. La lista de dependencias aprobadas y la inspección de imports lo previenen; HU-12 no agrega dependencias de producción.

6. Una métrica aislada puede pasar aunque el código tenga defectos; la complejidad no detecta reglas erróneas. Se necesitan pruebas, seguridad, estilo, dependencias y revisión en conjunto.

7. El experimento del grupo aún no se midió. Se completará el CSV antes de comparar con METR y DORA; no se inventa una conclusión sobre productividad.

8. La responsabilidad corresponde al equipo y a quienes aprueban e integran el cambio. ADR-012 exige compuertas, revisión humana y que nadie integre código que no pueda explicar.
