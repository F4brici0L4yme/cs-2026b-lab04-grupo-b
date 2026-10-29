"""Matriz de probabilidad/impacto, consistente con atam-lite.md."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

RIESGOS = {"R1": (4, 5), "R2": (3, 5), "R3": (4, 4), "R4": (3, 4),
           "R5": (4, 3), "R6": (3, 3), "R7": (3, 4)}

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(7.5, 5.8))
    ax.add_patch(Rectangle((2.5, 2.5), 3, 3, color="#f6ddd8", zorder=0))
    for nombre, (p, i) in RIESGOS.items():
        dx = -.18 if nombre == "R4" else .18 if nombre == "R7" else 0
        ax.scatter(p + dx, i, s=850, color="#b8402b", zorder=3)
        ax.text(p + dx, i, nombre, ha="center", va="center", color="white", weight="bold", zorder=4)
    ax.text(3.9, 5.25, "Zona crítica: P ≥3, I ≥3", fontsize=10)
    ax.set(xlim=(.5, 5.5), ylim=(.5, 5.5), xticks=range(1, 6), yticks=range(1, 6),
           xlabel="Probabilidad ordinal (1–5)", ylabel="Impacto (1–5)",
           title="Riesgos iniciales — RutaSIT Lab 08\nR3 y R5 mitigados en prototipo; residual en ATAM-lite")
    ax.grid(alpha=.25)
    fig.tight_layout()
    fig.savefig(Path(__file__).resolve().parents[1] / "docs/architecture/riesgos.png", dpi=160)
