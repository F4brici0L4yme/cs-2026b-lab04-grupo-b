"""Vista de despliegue (E6) — RutaSIT Arequipa.

Requiere: pip install diagrams + Graphviz (dot) en el sistema.
Uso: uv run --with diagrams python docs/architecture/diagramas/despliegue.py
Salida: docs/architecture/diagramas/img/despliegue.png
"""

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Mobile
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Celery
from diagrams.programming.framework import Django

SALIDA = Path(__file__).parent / "img" / "despliegue"

with Diagram("RutaSIT — Vista de despliegue", filename=str(SALIDA),
             show=False, direction="LR", outformat="png"):
    buses = Users("Buses GPS (300)")
    movil = Mobile("Pasajeros (móvil)")
    operador = Users("Operador")
    proxy = Nginx("Proxy HTTPS")
    with Cluster("VPS único (R-03)"):
        app = Django("API monolito modular")
        cache = Redis("Caché + cola")
        db = PostgreSQL("PostgreSQL")
        worker = Celery("Worker ETA/alertas")
        mon = Grafana("Monitoreo")
    with Cluster("Externos"):
        from diagrams.generic.blank import Blank
        mapas = Blank("Mapas abiertos")

    buses >> Edge(label="POST cada 10 s") >> proxy
    movil >> Edge(label="mapa + ETA") >> proxy
    operador >> Edge(label="panel") >> proxy
    proxy >> app
    app >> Edge(label="lee/escribe") >> db
    app >> Edge(label="encola") >> cache >> worker
    worker >> db
    app >> Edge(label="tiles") >> mapas
    app >> Edge(label="métricas") >> mon
