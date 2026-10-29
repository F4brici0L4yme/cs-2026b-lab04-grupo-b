# E6 — C4 actualizado

Fuente de partida: `lab06/docs/architecture/c4/workspace.dsl`. Fuente vigente
para Lab 08: [workspace.dsl](workspace.dsl). Las cinco vistas salen del mismo
modelo; exportaciones en `export/`, imágenes en `img/`.

| Vista | PNG | Fuente exportada |
|---|---|---|
| Contexto | [Imagen](img/structurizr-Contexto.png) | [PlantUML](export/structurizr-Contexto.puml) |
| Contenedores (requerida E6) | [Imagen](img/structurizr-Contenedores.png) | [PlantUML](export/structurizr-Contenedores.puml) |
| Componentes | [Imagen](img/structurizr-Componentes.png) | [PlantUML](export/structurizr-Componentes.puml) |
| Dinámica de actualización | [Imagen](img/structurizr-ActualizacionETA.png) | [PlantUML](export/structurizr-ActualizacionETA.puml) |
| Despliegue | [Imagen](img/structurizr-Despliegue.png) | [PlantUML](export/structurizr-Despliegue.puml) |

## Cambios trazables

- 300→1200 unidades en despliegue; mismo VPS y cuatro contenedores.
- API y worker incorporan las responsabilidades de ADR-006/007/008.
- API lee caché y read model; worker publica ETA reciente conservando captura.
- Mapas se protegen por breaker; la API produce respuesta textual degradada.
- Descripciones de actores, sistemas, contenedores y componentes indican `[QA-xx]`.
- Se exporta una dinámica enfocada en captura→ETA, que complementa la HU-06
  histórica. Las dependencias del diagrama de componentes son estáticas, no
  llamadas directas desde aplicación hacia implementaciones concretas.

## Correspondencia con el prototipo

`presentacion.py`, `aplicacion/`, `dominio.py` e `infraestructura/` implementan
el corte de lectura y mapas. `arranque.py` ensambla dependencias. Los tipos
Compartidos del diseño completo se representan aquí mediante identificadores
de texto del dominio; no se inventa un quinto paquete vacío.
Worker Celery, PostgreSQL y Redis siguen siendo **diseño objetivo**, no servicios
desplegados por este prototipo en memoria. Por ello `validate` demuestra validez
del modelo, no funcionamiento de la plataforma en producción.

## Reproducción desde la raíz

```bash
python lab08/scripts/modelo.py
python lab08/scripts/diagramas.py --plantuml /ruta/plantuml-1.2025.2.jar
```

Se fija el digest de la imagen Structurizr dentro de `modelo.py` para usar el
mismo exportador localmente y en CI. Requiere Docker, Java y Graphviz.
Salida real: [structurizr.txt](../../../evidencias/structurizr.txt).
