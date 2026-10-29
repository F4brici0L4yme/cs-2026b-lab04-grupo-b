"""Read model mínimo; no equivale a PostgreSQL/Redis desplegados."""

from rutasit8.dominio import LecturaETA


class RepositorioMemoria:
    def __init__(self):
        self.lecturas: dict[tuple[str, str], LecturaETA] = {}
        self.consultas = 0

    def guardar(self, lectura: LecturaETA) -> bool:
        clave = (lectura.bus_id, lectura.paradero_id)
        anterior = self.lecturas.get(clave)
        if anterior and (lectura.evento_id <= anterior.evento_id
                         or lectura.capturada_s < anterior.capturada_s):
            return False
        self.lecturas[clave] = lectura
        return True

    def obtener(self, bus_id: str, paradero_id: str) -> LecturaETA | None:
        self.consultas += 1
        return self.lecturas.get((bus_id, paradero_id))
