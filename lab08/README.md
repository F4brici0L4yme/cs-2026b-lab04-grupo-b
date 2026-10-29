# Laboratorio 08 — Diseño de arquitectura con ADD

**RutaSIT Arequipa · Grupo B · Construcción de Software · 2026-B**

[![fitness-functions](https://github.com/F4brici0L4yme/cs-2026b-lab04-grupo-b/actions/workflows/fitness.yml/badge.svg)](https://github.com/F4brici0L4yme/cs-2026b-lab04-grupo-b/actions/workflows/fitness.yml)

Continuación de los Labs 04–07: 1200 buses (120 eventos GPS/s) y 50 000 consultas
de ETA en hora punta. Se conserva monolito modular, Django/Celery, PostgreSQL y
Redis en un VPS. El código de esta carpeta es un prototipo en memoria y las
latencias son simuladas con supuestos explícitos; no son un benchmark de producción.

## Entregables

| E | Artefacto |
|---|---|
| E1 | [Entradas del Lab 04](docs/architecture/entradas.md), [escenarios](docs/architecture/utilidad/escenarios.md), [árbol DOT](docs/architecture/utilidad/arbol.dot) |
| E2 | [Iteración 1](docs/architecture/add/iteracion-1.md), [simulaciones](fitness/) |
| E3 | [ATAM-lite](docs/architecture/atam-lite.md), [intercambio externo pendiente](docs/architecture/revision-cruzada.md) |
| E4 | [Iteración 2](docs/architecture/add/iteracion-2.md), [iteración 3](docs/architecture/add/iteracion-3.md) |
| E5 | [Fitness functions](docs/architecture/fitness.md), [tests](tests/test_fitness.py), [contratos](../.importlinter), [workflow](../.github/workflows/fitness.yml) |
| E6 | [ADR-006](docs/architecture/adr/006-ingesta.md), [ADR-007](docs/architecture/adr/007-consultas-eta.md), [ADR-008](docs/architecture/adr/008-disponibilidad-mapas.md), [C4](docs/architecture/c4/README.md) |
| E7 | [Matriz/ATAM-lite](docs/architecture/atam-lite.md), [bitácora IA](docs/architecture/bitacora-ia.md) |
| E8 | [Entrega y colaboración](entrega.md), [fuente Markdown del informe](docs/informe.md); DOCX y PDF generados localmente en `informe/` (ignorados por Git) |

![Árbol de utilidad](docs/architecture/utilidad/arbol.png)

## Resultado por iteración

Semilla 7; resultados completos con tres semillas en [evidencias](evidencias/resultados.md).

| Iteración | Escenario | Táctica | Evidencia antes → después | ¿Cumple? |
|---|---|---|---|---|
| 1 | QA-01/03 | Reducir trabajo por evento; geometría precargada | p95 ráfaga 99,919→7,616 s | QA-01 sí en modelo; CPU QA-03 pendiente |
| 2 | QA-04/07 | Read model indexado + caché TTL 2 s, vigencia por captura | p95 pico base 1 496 233,391→130,788 ms; caché fría 256,663 ms | Sí bajo supuestos; sensibilidad de servicio registrada |
| 3 | QA-02 | Circuit breaker + estado textual | 1200→0 vistas vacías; 3600→42 llamadas | Sí en falla secuencial inyectada |

## Ejecutar desde la raíz del repositorio

Python 3.11+ (CI usa 3.12), Docker para C4; Graphviz/Java/LibreOffice para figuras e informe. Las dependencias Python del DOCX (`python-docx`, `Markdown`, `Pillow`) están incluidas en `lab08[dev]`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e './lab08[dev]'
.venv/bin/python lab08/scripts/verificar.py
.venv/bin/python lab08/scripts/probar_violaciones.py
.venv/bin/python -m fitness.experimentos
.venv/bin/python lab08/scripts/modelo.py
.venv/bin/python lab08/scripts/riesgos.py
.venv/bin/python lab08/scripts/diagramas.py --plantuml /ruta/plantuml-1.2025.2.jar
.venv/bin/python lab08/scripts/informe.py --plantilla '../Recursos/XX-CS-LAB PLANTILLA.docx'
libreoffice --headless --convert-to pdf --outdir lab08/informe lab08/informe/Informe_Lab08_GrupoB.docx
```

La plantilla institucional es opcional: si no está disponible, el generador usa
un documento nuevo con la misma información. [`docs/informe.md`](docs/informe.md)
es la fuente editable y versionada. La carpeta `informe/` se ignora por completo:
los PDF/DOCX se conservan solo localmente y deben compartirse aparte para la
entrega. La plantilla está fuera del repositorio, en `../Recursos/`. El prototipo
se instala como `rutasit8` para evitar conflictos con los dos paquetes
históricos `rutasit`.

## Verificación y pendientes

- Lab 08: **24 pruebas aprobadas**; **2 contratos cumplidos**.
- Violaciones: fallo esperado, reversión y recuperación verificados en rama temporal.
- Lab 05: **10 pruebas OK**. Lab 07: **30 passed, 1 xfailed preexistente**.
- Structurizr: validación exitosa y cinco vistas exportadas a PlantUML/Mermaid.
- Publicación, Action remoto verde, PR por persona, revisión externa y tag están
  pendientes: consultar [entrega.md](entrega.md). Ningún resultado local se presenta
  como revisión externa o ejecución remota.
