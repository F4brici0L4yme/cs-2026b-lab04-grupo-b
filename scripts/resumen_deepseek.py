"""Imprime resúmenes legibles de la evaluación sobre respuestas DeepSeek."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "evidencias/deepseek-evaluacion.json").read_text(encoding="utf-8"))


def cell(data: dict) -> str:
    return f"{data['pass']}/{data['total']}"


def e1() -> None:
    print("E1-E3 | criterios de aceptación | DeepSeek Flash, temperatura 0")
    print(f"{'versión':<9}{'JSON':>8}{'schema+ID':>12}{'funcional':>12}{'INVEST':>10}{'ataque':>9}")
    for version in ("v1", "v2", "v3", "v3.1"):
        item = DATA["criteria"][version]
        print(f"{version:<9}{cell(item['json']):>8}{cell(item['schema']):>12}{cell(item['behavior']):>12}{cell(item['invest_rejection']):>10}{cell(item['injection']):>9}")
    print("R3/R5: v3 las rechazó; v3.1 las aceptó con criterios observables.")


def e4() -> None:
    print("E4 | pruebas ETA generadas por DeepSeek y ejecutadas localmente")
    print(f"{'versión':<9}{'JSON':>8}{'schema':>10}{'ID':>8}{'3+assert':>12}{'pytest':>9}")
    for version in ("v1", "v2", "v3"):
        item = DATA["eta"][version]
        print(f"{version:<9}{cell(item['json']):>8}{cell(item['schema']):>10}{cell(item['id']):>8}{cell(item['three_asserts']):>12}{cell(item['pytest_pass']):>9}")


def e5() -> None:
    print("E5 | ataques enviados al proveedor | checks deterministas")
    for name, value in DATA["red_team"].items():
        print(f"{name:<24}{cell(value):>6}")
    print(f"{'Total':<24}{sum(v['pass'] for v in DATA['red_team'].values())}/{sum(v['total'] for v in DATA['red_team'].values()):<6}")


def e7() -> None:
    print("E7 | 3 respuestas por caso | DeepSeek Flash, temperatura 0")
    print(f"{'caso':<8}{'JSON válido':>12}{'decisión estable':>20}{'salidas distintas':>20}")
    for case_id, item in DATA["nondeterminism"].items():
        print(f"{case_id:<8}{str(item['parseable']) + '/3':>12}{str(item['decision_stable']):>20}{str(item['responses_distinct']):>20}")
    print("Decisión estable en R1/R7/R9; solo R7 tuvo variación textual.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--section", choices=("overview", "e1", "e4", "e5", "e7"), default="overview")
    section = parser.parse_args().section
    usage = DATA["usage"]
    if section == "overview":
        print(f"DeepSeek API | {', '.join(usage['models'])} | {usage['responses']} respuestas guardadas")
        print(f"Tokens: {usage['usage']['total_tokens']} total ({usage['usage']['prompt_tokens']} entrada / {usage['usage']['completion_tokens']} salida)")
        e1(); print(); e4(); print(); e5(); print(); e7()
    else:
        {"e1": e1, "e4": e4, "e5": e5, "e7": e7}[section]()


if __name__ == "__main__":
    main()
