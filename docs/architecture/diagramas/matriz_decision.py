"""Figura de la matriz de decisión ponderada (E2) — Laboratorio 04.

Caso: RutaSIT Arequipa. Reproduce la figura del Paso 4: el total ponderado de las
tres alternativas de estilo arquitectónico. Es "diagram as code": la figura se
regenera si cambian los pesos o los puntajes.

Uso:
    uv run python docs/architecture/diagramas/matriz_decision.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # sin pantalla: solo exporta el PNG
import matplotlib.pyplot as plt

# --- Criterios y pesos (deben sumar 100 %) --------------------------------
CRITERIOS: dict[str, float] = {
    "Rendimiento en tiempo real": 0.30,  # QA-01
    "Tiempo de entrega": 0.25,           # R-01
    "Costo operativo": 0.20,             # R-03
    "Simplicidad operativa": 0.15,       # R-02
    "Modificabilidad": 0.10,             # QA-03 / interoperabilidad
}

# --- Puntajes de 1 (muy malo) a 5 (excelente) -----------------------------
PUNTAJES: dict[str, dict[str, int]] = {
    "A. Monolito en capas": {
        "Rendimiento en tiempo real": 3,
        "Tiempo de entrega": 5,
        "Costo operativo": 5,
        "Simplicidad operativa": 5,
        "Modificabilidad": 2,
    },
    "B. Microservicios": {
        "Rendimiento en tiempo real": 5,
        "Tiempo de entrega": 2,
        "Costo operativo": 2,
        "Simplicidad operativa": 1,
        "Modificabilidad": 5,
    },
    "C. Monolito modular": {
        "Rendimiento en tiempo real": 4,
        "Tiempo de entrega": 4,
        "Costo operativo": 5,
        "Simplicidad operativa": 4,
        "Modificabilidad": 4,
    },
}

assert abs(sum(CRITERIOS.values()) - 1.0) < 1e-9, "Los pesos deben sumar 100 %"


def total_ponderado(puntajes: dict[str, int]) -> float:
    """Total ponderado = Σ (peso × puntaje)."""
    return sum(CRITERIOS[c] * puntajes[c] for c in CRITERIOS)


def main() -> None:
    totales = {alt: total_ponderado(p) for alt, p in PUNTAJES.items()}

    print("Criterio (peso)".ljust(32), "A".center(6), "B".center(6), "C".center(6))
    for criterio, peso in CRITERIOS.items():
        fila = [PUNTAJES[alt][criterio] for alt in PUNTAJES]
        print(f"{criterio} ({peso:.0%})".ljust(32), *(str(v).center(6) for v in fila))
    print("TOTAL PONDERADO".ljust(32), *(f"{totales[alt]:.2f}".center(6) for alt in totales))

    ganadora = max(totales, key=totales.get)
    print(f"\nAlternativa elegida: {ganadora} ({totales[ganadora]:.2f})")

    # --- Gráfico de barras horizontales ----------------------------------
    alternativas = list(totales.keys())
    valores = [totales[a] for a in alternativas]
    colores = ["#2E7D32" if a == ganadora else "#9E9E9E" for a in alternativas]

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    barras = ax.barh(alternativas, valores, color=colores, height=0.55)
    ax.set_xlim(0, 5)
    ax.set_xlabel("Total ponderado (1 = muy malo … 5 = excelente)")
    ax.set_title("Matriz de decisión ponderada — RutaSIT Arequipa", fontweight="bold")
    ax.axvline(x=valores[alternativas.index(ganadora)], color="#2E7D32",
               linestyle=":", linewidth=1)

    for barra, valor in zip(barras, valores):
        ax.text(valor + 0.06, barra.get_y() + barra.get_height() / 2,
                f"{valor:.2f}", va="center", fontsize=11, fontweight="bold")

    ax.invert_yaxis()
    fig.tight_layout()

    salida = Path(__file__).parent / "img" / "matriz-decision.png"
    salida.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(salida, dpi=200)
    print(f"\nFigura guardada en: {salida}")


if __name__ == "__main__":
    main()
