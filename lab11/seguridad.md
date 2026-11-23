# E7 — Seguridad y auditoría

- [x] Transporte `stdio` local; sin secretos ni llamadas de red.
- [x] Dos herramientas de solo lectura y exactamente una escritura.
- [x] `reportar_desvio` solo crea archivos nuevos numerados.
- [x] Entradas validan rutas, IDs, formato, longitud y traversal en ADR.
- [x] Recursos y descripciones se tratan como datos, no instrucciones.
- [x] La herramienta de escritura tiene `destructive_hint=False` y requiere aprobación del host.
- [x] El auditor comprueba escritura sin `destructiveHint` y texto libre sin límites; tras publicar `minLength`/`maxLength`, RutaSIT no presenta hallazgos.
- [x] Auditoría de host real: la escritura creó solamente `reportes/DESVIO-03.md` tras autorización explícita del usuario.

El auditor revisa instrucciones dirigidas al modelo, solicitudes de secretos, parámetros de texto libre sin límite y herramientas de escritura sin anotación explícita.

No se encontró el archivo `terceros/clima_mcp.py` mencionado por la guía en este repositorio, por lo que no se inventa una auditoría de tercero. Antes de conectar uno, se debe ejecutar el auditor sobre su catálogo y revisar sus descripciones.
