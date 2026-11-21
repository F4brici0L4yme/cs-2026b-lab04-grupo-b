"""Coordinación actor-crítico con ejecutor y revisor de solo lectura."""

from __future__ import annotations

from pathlib import Path

from agentes.agente.nucleo import Agente
from agentes.agente.politica import Politica


class OrquestadorActorCritico:
    def __init__(
        self,
        herramientas,
        fabrica_modelo,
        directorio_trazas: Path,
        max_rondas: int = 2,
    ):
        if not 1 <= max_rondas <= 2:
            raise ValueError("max_rondas debe estar entre 1 y 2")
        self.herramientas = herramientas
        self.fabrica_modelo = fabrica_modelo
        self.directorio_trazas = directorio_trazas
        self.max_rondas = max_rondas
        self.agentes: list[Agente] = []

    def ejecutar(self, objetivo: str) -> tuple[str, str]:
        planificador = Agente(
            nombre="planificador_issue02",
            modelo=self.fabrica_modelo("planificador", 1),
            herramientas=self.herramientas,
            politica=Politica(
                herramientas_permitidas=set(),
                max_pasos=2,
            ),
            objetivo=f"Propón un plan breve y verificable para este issue:\n{objetivo}",
            traza=self.directorio_trazas / "planificador_issue02.jsonl",
        )
        plan = planificador.ejecutar()
        self.agentes.append(planificador)
        retroalimentacion = ""
        resumen = ""
        veredicto = ""
        for ronda in range(1, self.max_rondas + 1):
            ejecutor = Agente(
                nombre=f"ejecutor_issue02_r{ronda}",
                modelo=self.fabrica_modelo("ejecutor", ronda),
                herramientas=self.herramientas,
                politica=Politica(max_pasos=12),
                objetivo=f"{objetivo}\n{plan}\n{retroalimentacion}",
                traza=self.directorio_trazas / f"ejecutor_issue02_r{ronda}.jsonl",
            )
            resumen = ejecutor.ejecutar()
            revisor = Agente(
                nombre=f"revisor_issue02_r{ronda}",
                modelo=self.fabrica_modelo("revisor", ronda),
                herramientas=self.herramientas,
                politica=Politica(
                    herramientas_permitidas={
                        "listar_archivos",
                        "leer_archivo",
                        "buscar",
                        "ejecutar_comando",
                        "ver_cambios",
                    },
                    max_pasos=8,
                ),
                objetivo=(
                    "Revisa el cambio del ejecutor sin editar. Inspecciona la "
                    "implementación y ejecuta la prueba del issue. Emite APROBADO "
                    "o CAMBIOS SOLICITADOS con evidencia.\n"
                    f"Resumen del ejecutor: {resumen}"
                ),
                traza=self.directorio_trazas / f"revisor_issue02_r{ronda}.jsonl",
            )
            veredicto = revisor.ejecutar()
            self.agentes.extend((ejecutor, revisor))
            if veredicto.startswith("APROBADO"):
                break
            retroalimentacion = f"Revisión de ronda {ronda}: {veredicto}"
        return resumen, veredicto
