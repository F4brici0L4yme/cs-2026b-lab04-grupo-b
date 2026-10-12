# Esqueleto Python de RutaSIT

Implementación didáctica del dominio y de los puertos de E1, compatible con Python 3.11+ y sin dependencias de ejecución externas.

## Módulos

- `dominio.py`: `Bus`, `Ruta`, `Paradero`, `UbicacionGPS`, `AlertaDesvio`, `Conductor`, `UsuarioSistema`, `ETA` y `EstadoBus`.
- `puertos.py`: Protocols `IRepositorioRutaSIT`, `IGpsProvider`, `INotificadorAlerta`, `IEstimadorETA` e `IReloj`.
- `servicios.py`: `ResultadoSeguimiento`, `SeguimientoService`, `MonitoreoController` y `RutaSITAPI`.
- `infraestructura.py`: adaptadores en memoria para ejecutar las pruebas sin servicios reales.
- `compartido.py`: alias opaco `Id`; no contiene PII.

Desde `lab05/`, ejecutar las pruebas con:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

`Ruta.esta_en_ruta` usa distancia aproximada a segmentos del trazado y `EstimadorETASimple` usa velocidad media fija. Son sustitutos de ejemplo, no implementaciones de producción.

Para ingeniería inversa, instalar la dependencia opcional `pylint` y ejecutar desde `lab05/`:

```bash
python -m pip install 'pylint>=3.3'
pyreverse -o puml -p rutasit src/rutasit
```

Pyreverse no conserva toda la semántica UML manual (por ejemplo, multiplicidades, composición y la realización de Protocols); ver [round-trip](../../round-trip.md).
