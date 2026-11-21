"""Convierte trazas JSONL en Mermaid sequenceDiagram editable."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def mermaid_desde_traza(archivo: Path) -> str:
    eventos = [
        json.loads(linea)
        for linea in archivo.read_text(encoding="utf-8").splitlines()
        if linea.strip()
    ]
    agentes = sorted({str(e.get("agente", "agente")) for e in eventos})

    def prefijo(agente: str) -> str:
        if agente.startswith("planificador"):
            return "P"
        if agente.startswith("revisor"):
            return "R"
        if agente.startswith("ejecutor"):
            return "E"
        return "A"

    conteo: dict[str, int] = {}
    participantes = {}
    for agente in agentes:
        rol = prefijo(agente)
        conteo[rol] = conteo.get(rol, 0) + 1
        participantes[agente] = f"{rol}{conteo[rol]}"
    lineas = ["sequenceDiagram", "    actor Humano"]
    for agente in agentes:
        nombre = agente.replace("_", " ")
        lineas.append(f"    participant {participantes[agente]} as {nombre}")
    lineas.extend(
        [
            "    participant C as Contrato y política",
            "    participant H as Herramientas",
            f"    Humano->>{participantes[agentes[0]]}: Objetivo y límites",
        ]
    )
    for evento in eventos:
        paso = evento.get("paso", "?")
        accion = evento.get("accion")
        estado = evento.get("estado", "OBSERVANDO")
        agente = participantes.get(str(evento.get("agente", "agente")), "A")
        if accion:
            lineas.append(f"    {agente}->>C: Paso {paso}: validar {accion}")
            if evento.get("bloqueada"):
                observacion = str(evento.get("observacion", "bloqueada")).replace("\n", " ")[:90]
                lineas.append(f"    C-->>{agente}: {estado}: {observacion}")
            else:
                lineas.append(f"    C-->>{agente}: permitido")
                lineas.append(f"    {agente}->>H: {accion}")
                observacion = str(evento.get("observacion", "ok")).replace("\n", " ")[:90]
                lineas.append(f"    H-->>{agente}: {observacion}")
        elif estado == "CONTRATO_INVALIDO":
            lineas.append(f"    {agente}->>C: Paso {paso}: validar decisión")
            lineas.append(f"    C-->>{agente}: decisión rechazada")
        elif evento.get("texto"):
            final = str(evento["texto"]).replace("\n", " ")[:120]
            lineas.append(f"    {agente}-->>Humano: {final}")
    return "\n".join(lineas) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("traza", type=Path)
    parser.add_argument("salida", type=Path)
    args = parser.parse_args()
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(mermaid_desde_traza(args.traza), encoding="utf-8")
    print(f"Diagrama Mermaid escrito en {args.salida}")


if __name__ == "__main__":
    main()
