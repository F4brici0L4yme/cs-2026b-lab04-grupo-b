"""Genera tablas, datos JSON y gráficos desde las simulaciones ejecutadas."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fitness.disponibilidad import simular
from fitness.rendimiento import simular_consultas, simular_ingesta

BASE = Path(__file__).resolve().parents[1]
SALIDA = BASE / "evidencias"


def main():
    SALIDA.mkdir(exist_ok=True)
    ingesta = [{"modo": modo, "buses": buses, "rafagas": rafagas, "semilla": semilla,
                **simular_ingesta(modo, buses=buses, rafagas=rafagas, semilla=semilla)}
               for buses in (300, 600, 1200) for modo in ("base", "optimizada")
               for rafagas in (False, True) for semilla in (7, 19, 42)]
    consultas = [{"modo": modo, "factor_pico": pico, "aciertos": aciertos, "semilla": semilla,
                  **simular_consultas(modo, tasa=pico * 50000 / 3600,
                                      aciertos=aciertos, semilla=semilla)}
                 for pico in (1, 5) for modo in ("base", "indice", "solo_cache", "indice_cache")
                 for aciertos in (0, .2, .8) for semilla in (7, 19, 42)]
    sensibilidad = [{"factor_servicio": factor,
                     "ingesta": simular_ingesta(rafagas=True, factor_servicio=factor),
                     "consultas": simular_consultas(tasa=5 * 50000 / 3600,
                                                     aciertos=0, factor_servicio=factor)}
                    for factor in (1, 1.5, 2, 3)]
    disponibilidad = {modo: simular(modo) for modo in ("base", "reintentos", "fallback", "breaker")}
    datos = {"tipo": "Simulación con parámetros hipotéticos, no benchmark del VPS",
             "semillas": [7, 19, 42], "ingesta": ingesta, "consultas": consultas,
             "sensibilidad_servicio": sensibilidad, "disponibilidad": disponibilidad}
    (SALIDA / "resultados.json").write_text(json.dumps(datos, indent=2, ensure_ascii=False) + "\n")
    tabla = ["# Resultados ejecutados — E2/E4", "",
             "Generado con `python -m fitness.experimentos`. Tiempos simulados; semilla 7 en las tablas.",
             "El JSON contiene las tres semillas y todos los casos. No son mediciones de producción.", "",
             "## Ingesta: 1200 buses, 300 s, 36 000 eventos", "",
             "| Configuración | Llegadas | p95 extremo a extremo (s) | % ≤15 s | Eventos fuera de cierre+15 s por minuto | Pendientes a 300 s |",
             "|---|---|---:|---:|---|---:|"]
    seleccion = [r for r in ingesta if r["buses"] == 1200 and r["semilla"] == 7]
    for r in seleccion:
        tabla.append(f'| {r["modo"]} | {"ráfaga" if r["rafagas"] else "fases"} | {r["p95_s"]:.3f} | '
                     f'{r["porcentaje_dentro_15s"]:.2f} | {r["pendientes_fuera_plazo_por_minuto"]} | '
                     f'{r["pendientes_al_cierre"]} |')
    tabla += ["", "## Consultas: p95 (ms), 300 s por ensayo", "",
              "| Configuración | Aciertos | 13,89 req/s | 69,44 req/s (pico ×5) |",
              "|---|---:|---:|---:|"]
    filas = []
    for modo, aciertos in (("base", 0), ("indice", 0), ("solo_cache", .8),
                            ("indice_cache", .8), ("indice_cache", 0)):
        rs = [next(r for r in consultas if r["modo"] == modo and r["aciertos"] == aciertos
                   and r["factor_pico"] == pico and r["semilla"] == 7) for pico in (1, 5)]
        filas.append((modo, aciertos, rs))
        tabla.append(f'| {modo} | {aciertos:.0%} | {rs[0]["p95_ms"]:.3f} | {rs[1]["p95_ms"]:.3f} |')
    tabla += ["", "## Mapas: caída de 1200 s durante 1800 consultas", "",
              "| Configuración | Pantallas vacías | Llamadas durante caída | Recuperación (s) |",
              "|---|---:|---:|---:|"]
    for modo, r in disponibilidad.items():
        tabla.append(f'| {modo} | {r["pantallas_vacias"]} | {r["llamadas_en_caida"]} | {r["recuperacion_s"]} |')
    tabla += ["", "## Sensibilidad: multiplicar tiempos de servicio", "",
              "| Factor | Ingesta sincronizada p95 (s) | Consultas ×5, caché fría p95 (ms) |",
              "|---|---:|---:|"]
    for r in sensibilidad:
        tabla.append(f'| {r["factor_servicio"]} | {r["ingesta"]["p95_s"]:.3f} | {r["consultas"]["p95_ms"]:.3f} |')
    (SALIDA / "resultados.md").write_text("\n".join(tabla) + "\n")

    fig, ax = plt.subplots(figsize=(9, 4.6))
    etiquetas = [r["modo"] + ("\nráfaga" if r["rafagas"] else "\nfases") for r in seleccion]
    barras = ax.bar(etiquetas, [r["p95_s"] for r in seleccion], color=["#c14937"] * 2 + ["#267b57"] * 2)
    ax.bar_label(barras, fmt="%.2f s", padding=3)
    ax.axhline(15, color="black", linestyle="--", label="QA-01: 15 s")
    ax.set(ylabel="p95 desde captura hasta consulta (s)", title="Ingesta simulada — 1200 buses / semilla 7")
    ax.legend()
    fig.tight_layout()
    fig.savefig(SALIDA / "ingesta.png", dpi=160)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (modo, aciertos, rs) in enumerate(filas):
        ax.bar([i - .18, i + .18], [r["p95_ms"] for r in rs], width=.35,
               color=["#326da8", "#da9140"])
    ax.set_xticks(range(len(filas)), [f"{m}\n{a:.0%} aciertos" for m, a, _ in filas])
    ax.set(yscale="log", ylabel="p95 (ms, escala logarítmica)",
           title="Consultas simuladas: azul 13,89 req/s; naranja 69,44 req/s")
    ax.axhline(2000, color="black", linestyle="--", label="QA-04: 2000 ms")
    ax.legend()
    fig.tight_layout()
    fig.savefig(SALIDA / "consultas.png", dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for ax, clave, titulo in zip(axes, ("pantallas_vacias", "llamadas_en_caida"),
                                ("Pantallas vacías", "Llamadas al proveedor caído")):
        b = ax.bar(list(disponibilidad), [r[clave] for r in disponibilidad.values()], color="#326da8")
        ax.bar_label(b, padding=3)
        ax.set_title(titulo)
        ax.tick_params(axis="x", rotation=20)
        ax.margins(y=.15)
    fig.tight_layout()
    fig.savefig(SALIDA / "disponibilidad.png", dpi=160)
    plt.close(fig)
    print(SALIDA / "resultados.md")


if __name__ == "__main__":
    main()
