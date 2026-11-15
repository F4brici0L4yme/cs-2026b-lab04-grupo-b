"""Genera el gráfico E8 desde el JSON de evaluación de respuestas originales."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "evidencias/deepseek-evaluacion.json").read_text(encoding="utf-8"))
WIDTH, HEIGHT = 960, 450
LEFT, TOP, PLOT_W, PLOT_H = 100, 100, 820, 270
BOTTOM = TOP + PLOT_H


def pct(item: dict) -> float:
    return 100 * item["pass"] / item["total"] if item["total"] else 0


categories = []
for version, label in (("v1", "A v1"), ("v2", "A v2"), ("v3", "A v3"), ("v3.1", "A v3.1")):
    item = DATA["criteria"][version]
    categories.append((label, pct(item["json"]), pct(item["behavior"])))
for version, label in (("v1", "ETA v1"), ("v2", "ETA v2"), ("v3", "ETA v3")):
    item = DATA["eta"][version]
    categories.append((label, pct(item["json"]), pct(item["pytest_pass"])))

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
    '<rect width="100%" height="100%" fill="white"/>',
    '<text x="480" y="34" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold">Lab 09 — DeepSeek: tasa por versión</text>',
    '<text x="480" y="59" text-anchor="middle" font-family="Arial" font-size="13">deepseek-flash · temperatura 0 · aserciones deterministas sobre salidas guardadas</text>',
]
for value in (0, 25, 50, 75, 100):
    y = BOTTOM - PLOT_H * value / 100
    parts.append(f'<line x1="{LEFT}" y1="{y}" x2="{LEFT + PLOT_W}" y2="{y}" stroke="#ddd"/>')
    parts.append(f'<text x="{LEFT - 18}" y="{y + 4}" text-anchor="end" font-family="Arial" font-size="12" fill="#222">{value}</text>')
parts.extend([
    f'<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{BOTTOM}" stroke="#333"/>',
    f'<line x1="{LEFT}" y1="{BOTTOM}" x2="{LEFT + PLOT_W}" y2="{BOTTOM}" stroke="#333"/>',
    '<text x="28" y="91" font-family="Arial" font-size="12">%</text>',
])
step = PLOT_W / len(categories)
bar_w = 28
for index, (label, json_pct, quality_pct) in enumerate(categories):
    center = LEFT + step * (index + 0.5)
    for offset, value, color in ((-bar_w / 2, json_pct, "#d95f02"), (bar_w / 2, quality_pct, "#1b9e77")):
        x = center + offset
        h = PLOT_H * value / 100
        y = BOTTOM - h
        parts.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" fill="{color}"/>')
    parts.append(f'<text x="{center}" y="{BOTTOM + 24}" text-anchor="middle" font-family="Arial" font-size="12">{label}</text>')
parts.extend([
    '<rect x="300" y="422" width="14" height="14" fill="#d95f02"/><text x="320" y="434" font-family="Arial" font-size="12">JSON válido</text>',
    '<rect x="470" y="422" width="14" height="14" fill="#1b9e77"/><text x="490" y="434" font-family="Arial" font-size="12">Criterios funcionales / pytest</text>',
    '</svg>',
])
(ROOT / "docs/lab09/evaluacion.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")
print("docs/lab09/evaluacion.svg actualizado desde evidencias/deepseek-evaluacion.json")
