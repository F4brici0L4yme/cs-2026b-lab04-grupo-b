"""Política por rol: límites de pasos, comandos y rutas editables."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Decision:
    permitido: bool
    motivo: str = ""


def aprobar_en_consola(args: dict[str, object], input_fn=input, output_fn=print) -> bool:
    while True:
        output_fn(f"¿Aprobar edición de {args.get('ruta', '')}? [s/n]")
        respuesta = input_fn().strip().lower()
        if respuesta == "s":
            return True
        if respuesta == "n":
            return False
        output_fn("Respuesta inválida; escriba solo s o n.")


@dataclass
class Politica:
    herramientas_permitidas: set[str] = field(
        default_factory=lambda: {
            "listar_archivos",
            "leer_archivo",
            "buscar",
            "mapa_repo",
            "editar_archivo",
            "ejecutar_comando",
            "ver_cambios",
            "anotar",
            "leer_notas",
        }
    )
    comandos_permitidos: tuple[str, ...] = (
        r"^python(?:3)? -m pytest -c lab09/pyproject\.toml -q (?:lab09/tests/test_issue_[0-9]{2}_[a-z_]+\.py|agentes/pruebas_agente)$",
        r"^python(?:3)? -m pytest -c lab09/pyproject\.toml -q lab09/tests$",
        r"^radon cc -s lab09/caso_rutasit/src$",
        r"^git status --short$",
        r"^git diff --stat$",
    )
    rutas_protegidas: tuple[str, ...] = ("tests/", "issues/", ".git/")
    rutas_editables: tuple[str, ...] = ("lab09/caso_rutasit/src/",)
    max_pasos: int = 12
    aprobar_edicion: Callable[[dict[str, object]], bool] | None = None

    def evaluar(
        self,
        accion: str,
        args: dict[str, object],
        paso: int,
        raiz: Path,
    ) -> Decision:
        if paso > self.max_pasos:
            return Decision(False, f"Se alcanzó el máximo de {self.max_pasos} pasos")
        if accion not in self.herramientas_permitidas:
            return Decision(False, f"Herramienta no permitida: {accion}")
        if accion == "ejecutar_comando":
            comando = args.get("comando", "")
            if not isinstance(comando, str) or not any(
                re.fullmatch(patron, comando) for patron in self.comandos_permitidos
            ):
                return Decision(False, f"Comando fuera de la lista permitida: {comando!r}")
        if accion == "editar_archivo":
            ruta = args.get("ruta", "")
            if not isinstance(ruta, str):
                return Decision(False, "ruta debe ser texto")
            destino = (raiz / ruta).resolve()
            try:
                relativa = destino.relative_to(raiz.resolve()).as_posix()
            except ValueError:
                return Decision(False, f"Ruta fuera del sandbox: {ruta}")
            partes = Path(relativa).parts
            if any(Path(protegida.rstrip("/")).name in partes for protegida in self.rutas_protegidas):
                return Decision(False, f"Ruta protegida: {relativa}")
            if not any(relativa.startswith(prefijo) for prefijo in self.rutas_editables):
                return Decision(False, f"Ruta no editable por este agente: {relativa}")
            if self.aprobar_edicion and not self.aprobar_edicion(args):
                return Decision(False, "El revisor humano rechazó la edición")
        return Decision(True)
