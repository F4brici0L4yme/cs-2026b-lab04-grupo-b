# Código de integración RutaSIT

`GeneradorPrompt` usa plantillas por tarea y versión a través del puerto `ProveedorLLM`. Se incluyen las plantillas v3 y v3.1 para criterios de aceptación, la plantilla v3 para pruebas ETA, y los esquemas JSON junto a las plantillas en `prompts/criterios/esquema.json` y `prompts/pruebas_eta/esquema.json`.

Dependencias: Python 3.10+ y `jsonschema`.

Las pruebas con `ProveedorGrabado` y el workflow están en el repositorio del grupo (`tests/test_generador_prompt.py`, `.github/workflows/lab09-manual.yml`). No requieren una clave de API.
