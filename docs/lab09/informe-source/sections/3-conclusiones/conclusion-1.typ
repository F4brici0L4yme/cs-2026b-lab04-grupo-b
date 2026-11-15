Las respuestas originales de DeepSeek permitieron medir cada iteración con el mismo conjunto. v3.1 de criterios aprobó 9/9 casos luego de que v3 rechazara R3 y R5; v3 de ETA aprobó las ocho pruebas ejecutables. Los porcentajes corresponden a estas entradas y aserciones.

La integración detrás de `ProveedorLLM` añade una barrera útil: el consumidor recibe una salida solo después de parsear JSON y validar el contrato. Las pruebas con proveedor grabado cubren aceptación de salida válida y rechazo de salidas inválidas; la defensa debe complementarse con revisión humana y casos adversarios.

Las cinco respuestas al red team pasaron los criterios definidos para inyección directa e indirecta, extracción, formato y lenguaje. La muestra respalda las defensas probadas, aunque no cubre todas las variantes de ataque. Conservar las respuestas y metadatos permite repetir las aserciones sin volver a llamar al proveedor.

El PR #4 fue aprobado y fusionado por Brayan, y `v0.9-prompts` quedó publicado sobre ese commit. El grupo debe registrar en Aula Virtual el enlace del repositorio y este informe.
