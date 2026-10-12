"""Tipos compartidos por las capas de RutaSIT."""

from typing import NewType

Id = NewType("Id", str)
"""Identificador opaco; no contiene nombre, DNI ni teléfono."""
