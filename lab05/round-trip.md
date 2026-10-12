# Round-trip: ingeniería inversa de RutaSIT

## Comando ejecutado

Con `pylint` instalado (incluye Pyreverse), desde `lab05/`:

```bash
pyreverse -o puml -p rutasit src/rutasit
```

Pyreverse analizó los seis módulos de `src/rutasit/` y produjo los diagramas de clases y paquetes, guardados como [`classes_rutasit.puml`](roundtrip/classes_rutasit.puml) y [`packages_rutasit.puml`](roundtrip/packages_rutasit.puml). La salida inversa se usa como contraste; `diagrama_clases.puml` y `diagrama_paquetes.puml` siguen siendo los modelos fuente corregidos manualmente.

El comando solicitado escribe los dos archivos en el directorio de trabajo; después de ejecutarlo desde `lab05/`, se movieron a `roundtrip/` para separarlos de los diagramas fuente.

## Diferencias identificadas

| Diferencia / discrepancia | Causa raíz | Acción tomada |
|---|---|---|
| Pyreverse no expresa las multiplicidades ni distingue todas las asociaciones, agregaciones y composiciones del modelo inicial. | Las anotaciones Python indican tipos, pero no contienen por sí solas las multiplicidades y la semántica de ciclo de vida UML. | **Corregir y conservar el diagrama manualmente.** Las multiplicidades y relaciones se especifican en `diagrama_clases.puml`; no se infieren del código. |
| Los `Protocol` (`IGpsProvider`, `INotificadorAlerta`, etc.) aparecen como clases y Pyreverse no dibuja todas las realizaciones de los adaptadores. | Pyreverse no traduce automáticamente cada `typing.Protocol` a una interfaz UML con relaciones `..|>`. | **Documentar limitación y mantener las realizaciones explícitas** en `diagrama_clases.puml` y `diagrama_paquetes.puml`. |
| Algunos atributos de dataclasses, como `Bus.estado` y `AlertaDesvio.ubicacion`, aparecen sin tipo; los valores del enum tampoco se expanden en la salida inversa. | Limitación de la inferencia de Pyreverse al combinar dataclasses, anotaciones pospuestas (`from __future__ import annotations`), `NewType` y `Enum`. | **Documentar limitación.** Se conserva la tipificación explícita y los valores del enum en el modelo inicial; el código no se altera para acomodar la salida incompleta de la herramienta. |

La revisión no encontró una diferencia de comportamiento que requiriera cambiar el código fuente. La ingeniería inversa es una vista parcial y no reemplaza el modelo UML validado contra C1-C5.

Pyreverse también muestra el paquete Python superior `rutasit` porque representa la estructura de módulos. En E5 se omite como capa arquitectónica: las cinco capas solicitadas son paquetes conceptuales, mientras que `rutasit/` es el namespace técnico del código.
