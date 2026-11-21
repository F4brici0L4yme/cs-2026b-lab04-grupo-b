"""Reproduce las trayectorias de los tres issues y la comparación de E5."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

from agentes.agente.herramientas import Herramientas
from agentes.agente.modelos import ModeloGrabado, ModeloInteractivo
from agentes.agente.nucleo import Agente
from agentes.agente.politica import Politica
from agentes.orquestador import OrquestadorActorCritico


def restablecer_funcion_inicial(raiz: Path, nombre_funcion: str) -> None:
    fuente = raiz / "lab09/caso_rutasit/src/rutasit_demo/seguimiento.py"
    base = raiz / "lab09/caso_rutasit/fixtures/seguimiento_inicial.py"
    contenido = fuente.read_text(encoding="utf-8")
    inicial = base.read_text(encoding="utf-8")
    nodo_actual = next(
        nodo for nodo in ast.parse(contenido).body
        if isinstance(nodo, ast.FunctionDef) and nodo.name == nombre_funcion
    )
    nodo_base = next(
        nodo for nodo in ast.parse(inicial).body
        if isinstance(nodo, ast.FunctionDef) and nodo.name == nombre_funcion
    )
    lineas_actuales = contenido.splitlines(keepends=True)
    lineas_base = inicial.splitlines(keepends=True)
    fuente.write_text(
        "".join(
            lineas_actuales[: nodo_actual.lineno - 1]
            + lineas_base[nodo_base.lineno - 1 : nodo_base.end_lineno]
            + lineas_actuales[nodo_actual.end_lineno :]
        ),
        encoding="utf-8",
    )


def ejecutar_issue(
    raiz: Path,
    id_issue: str,
    interactivo: bool = False,
) -> str:
    funcion_issue = {
        "issue01": "calcular_eta_minutos",
        "issue02_unico": "esta_en_ruta",
        "issue03": "crear_respuesta_gps",
    }
    restablecer_funcion_inicial(raiz, funcion_issue[id_issue])
    trayectoria = raiz / "agentes/trayectorias" / f"{id_issue}.json"
    decisiones = json.loads(trayectoria.read_text(encoding="utf-8"))["decisiones"]
    if interactivo:
        respuestas = iter(json.dumps(d, ensure_ascii=False) for d in decisiones)
        modelo = ModeloInteractivo(input_fn=lambda: next(respuestas), output_fn=lambda _: None)
    else:
        modelo = ModeloGrabado(trayectoria)
    agente = Agente(
        nombre=f"ejecutor_{id_issue}",
        modelo=modelo,
        herramientas=Herramientas(raiz),
        politica=Politica(max_pasos=12),
        objetivo=f"Resuelve {id_issue} de RutaSIT. No edites pruebas.",
        traza=raiz / "agentes/trazas" / f"{id_issue}.jsonl",
    )
    respuesta = agente.ejecutar()
    print(respuesta)
    return respuesta


def ejecutar_actor(raiz: Path) -> tuple[str, str]:
    restablecer_funcion_inicial(raiz, "esta_en_ruta")
    archivo = raiz / "agentes/trayectorias/actor_issue02.json"
    datos = json.loads(archivo.read_text(encoding="utf-8"))

    def modelo_por_rol(rol: str, ronda: int):
        claves = {
            ("planificador", 1): "planificador_issue02",
            ("ejecutor", 1): "executor_r1",
            ("revisor", 1): "reviewer_r1",
            ("ejecutor", 2): "executor_r2",
            ("revisor", 2): "reviewer_r2",
        }
        clave = claves[(rol, ronda)]
        decisiones = (
            json.loads((raiz / "agentes/trayectorias/planificador_issue02.json").read_text(encoding="utf-8"))["decisiones"]
            if clave == "planificador_issue02"
            else datos[clave]
        )
        return ModeloGrabado(decisiones)

    orquestador = OrquestadorActorCritico(
        herramientas=Herramientas(raiz),
        fabrica_modelo=modelo_por_rol,
        directorio_trazas=raiz / "agentes/trazas",
        max_rondas=2,
    )
    resultado = orquestador.ejecutar(
        "ISSUE-02: el bus dentro de una curva se marca fuera de ruta; "
        "la distancia debe calcularse a segmentos."
    )
    print(f"EJECUTOR: {resultado[0]}\nREVISOR: {resultado[1]}")
    return resultado


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "accion",
        choices={"todo", "issue01-interactivo", "issue02-unico", "issue02-actor", "issue03"},
    )
    parser.add_argument("--raiz", type=Path, default=Path.cwd())
    args = parser.parse_args()
    if args.accion == "todo":
        ejecutar_issue(args.raiz, "issue01", interactivo=True)
        ejecutar_issue(args.raiz, "issue02_unico")
        ejecutar_actor(args.raiz)
        ejecutar_issue(args.raiz, "issue03")
    elif args.accion == "issue01-interactivo":
        ejecutar_issue(args.raiz, "issue01", interactivo=True)
    elif args.accion == "issue02-unico":
        ejecutar_issue(args.raiz, "issue02_unico")
    elif args.accion == "issue02-actor":
        ejecutar_actor(args.raiz)
    else:
        ejecutar_issue(args.raiz, "issue03")


if __name__ == "__main__":
    main()
