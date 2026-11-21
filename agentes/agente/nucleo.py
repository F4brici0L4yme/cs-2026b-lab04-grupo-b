"""Bucle ReAct acotado con contrato, política y traza JSONL."""

from __future__ import annotations

import json
from pathlib import Path

from .contrato import validar_decision
from .herramientas import Herramientas
from .politica import Politica


class Agente:
    def __init__(
        self,
        nombre: str,
        modelo,
        herramientas: Herramientas,
        politica: Politica,
        objetivo: str,
        traza: Path,
    ):
        self.nombre = nombre
        self.modelo = modelo
        self.herramientas = herramientas
        self.politica = politica
        self.historial = [{"role": "user", "content": objetivo}]
        self.traza = traza
        self.eventos: list[dict[str, object]] = []

    def _registrar(self, evento: dict[str, object]) -> None:
        evento = {"agente": self.nombre, **evento}
        self.eventos.append(evento)

    def ejecutar(self) -> str:
        conocidas = set(self.herramientas.catalogo()) | {"final"}
        respuesta = "(sin respuesta final)"
        for paso in range(1, self.politica.max_pasos + 1):
            decision = self.modelo.decidir(self.historial)
            serializada = json.dumps(decision, ensure_ascii=False, default=str)
            self.historial.append({"role": "assistant", "content": serializada})
            valido, motivo = validar_decision(decision, conocidas)
            if not valido:
                observacion = f"ERROR DE CONTRATO: {motivo}. Responda solo con JSON válido."
                self._registrar(
                    {
                        "paso": paso,
                        "estado": "CONTRATO_INVALIDO",
                        "decision": decision,
                        "observacion": observacion,
                        "bloqueada": True,
                    }
                )
                self.historial.append({"role": "user", "content": f"Observación: {observacion}"})
                continue
            if "final" in decision:
                respuesta = decision["final"]
                self._registrar(
                    {
                        "paso": paso,
                        "estado": "FINALIZADO",
                        "pensamiento": decision["pensamiento"],
                        "texto": respuesta,
                        "bloqueada": False,
                        "contexto_caracteres": sum(len(m["content"]) for m in self.historial),
                    }
                )
                break
            accion = decision["accion"]
            args = decision.get("args", {})
            permiso = self.politica.evaluar(accion, args, paso, self.herramientas.raiz)
            if not permiso.permitido:
                observacion = f"BLOQUEADO POR LA POLÍTICA: {permiso.motivo}"
                bloqueada = True
                estado = "BLOQUEADO"
            else:
                try:
                    observacion = getattr(self.herramientas, accion)(**args)
                except Exception as error:
                    observacion = f"ERROR: {type(error).__name__}: {error}"
                bloqueada = False
                estado = "OBSERVANDO"
            self._registrar(
                {
                    "paso": paso,
                    "estado": estado,
                    "pensamiento": decision["pensamiento"],
                    "accion": accion,
                    "args": args,
                    "observacion": str(observacion)[:1000],
                    "bloqueada": bloqueada,
                }
            )
            self.historial.append({"role": "user", "content": f"Observación: {observacion}"})
        else:
            respuesta = f"Se alcanzó el límite de {self.politica.max_pasos} pasos."
            self._registrar(
                {
                    "paso": self.politica.max_pasos,
                    "estado": "LIMITE_ALCANZADO",
                    "texto": respuesta,
                    "bloqueada": True,
                    "contexto_caracteres": sum(len(m["content"]) for m in self.historial),
                }
            )
        self.traza.parent.mkdir(parents=True, exist_ok=True)
        self.traza.write_text(
            "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in self.eventos),
            encoding="utf-8",
        )
        return respuesta
