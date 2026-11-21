"""Ejecuta un agente interactivo o una trayectoria JSON grabada."""

from __future__ import annotations

import argparse
from pathlib import Path

from agentes.agente.herramientas import Herramientas
from agentes.agente.modelos import ModeloGrabado, ModeloInteractivo
from agentes.agente.nucleo import Agente
from agentes.agente.politica import Politica, aprobar_en_consola


def crear_agente(
    raiz: Path,
    objetivo: str,
    ruta_traza: Path,
    interactivo: bool,
    aprobar_ediciones: bool,
    trayectoria: Path | None = None,
) -> Agente:
    herramientas = Herramientas(raiz)
    if interactivo:
        modelo = ModeloInteractivo()
    elif trayectoria:
        modelo = ModeloGrabado(trayectoria)
    else:
        raise ValueError("Use --interactivo o --trayectoria")
    politica = Politica(
        max_pasos=12,
        aprobar_edicion=aprobar_en_consola if aprobar_ediciones else None,
    )
    return Agente(
        nombre="ejecutor",
        modelo=modelo,
        herramientas=herramientas,
        politica=politica,
        objetivo=objetivo,
        traza=ruta_traza,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raiz", type=Path, default=Path.cwd())
    parser.add_argument("--objetivo", required=True)
    parser.add_argument("--traza", type=Path, required=True)
    parser.add_argument("--interactivo", action="store_true")
    parser.add_argument("--trayectoria", type=Path)
    parser.add_argument("--aprobar-ediciones", action="store_true")
    args = parser.parse_args()
    agente = crear_agente(
        raiz=args.raiz,
        objetivo=args.objetivo,
        ruta_traza=args.traza,
        interactivo=args.interactivo,
        aprobar_ediciones=args.aprobar_ediciones,
        trayectoria=args.trayectoria,
    )
    print(agente.ejecutar())


if __name__ == "__main__":
    main()
