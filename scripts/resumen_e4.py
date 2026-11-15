"""Imprime la matriz compacta de resultados E4 guardada por el evaluador."""
import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
data = json.loads((root / "evidencias/e4-manual.json").read_text(encoding="utf-8"))
columns = ("json", "id", "three_asserts", "pytest_pass")
labels = ("JSON", "ID", "3+ asserts", "pytest")
print("E4 | checks locales sobre respuestas guardadas")
print(f"{'Version':<9}" + "".join(f"{label:>14}" for label in labels))
for version, results in data["results"].items():
    values = []
    for key in columns:
        item = results[key]
        values.append(f"{item['pass']}/{item['total']}")
    print(f"{version:<9}" + "".join(f"{value:>14}" for value in values))
