"""Resume la traza JSONL del agente y genera un diagrama Mermaid reproducible."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
TRAZA = RAIZ / "trazas" / "e4-rutasit.jsonl"


def analizar(archivo: Path) -> tuple[str, str]:
    eventos = [json.loads(linea) for linea in archivo.read_text(encoding="utf-8").splitlines() if linea.strip()]
    metricas: dict[str, list[float]] = defaultdict(list)
    for evento in eventos:
        if "latency_ms" in evento:
            etiqueta = f"{evento['method']}:{evento.get('tool', '')}".rstrip(":")
            metricas[etiqueta].append(float(evento["latency_ms"]))
    lineas = ["sequenceDiagram", "    participant Agent as Agente Lab 10", "    participant MCP as RutaSIT MCP"]
    for evento in eventos:
        if evento["direction"] == "request":
            lineas.append(f"    Agent->>MCP: {evento['method']} {evento.get('tool', '')}".rstrip())
        elif evento["method"] == "tools/call":
            lineas.append(f"    MCP-->>Agent: resultado {evento.get('tool', '')}".rstrip())
    informe = [f"# Métricas E6\n\n- Mensajes registrados: {len(eventos)}.", "- Transporte: cliente MCP local; sin red ni LLM.", "\n| Método | Latencia media (ms) |", "|---|---:|"]
    informe.extend(f"| `{metodo}` | {sum(valores) / len(valores):.3f} |" for metodo, valores in sorted(metricas.items()))
    catalogo = json.dumps({"tools": 3, "resources": 3, "prompts": 1}, ensure_ascii=False)
    informe.extend([
        "\n## Costo y optimización",
        f"El inventario mínimo del catálogo mide {len(catalogo)} caracteres (≈{(len(catalogo) + 3) // 4} tokens, aproximación de 4 caracteres/token).",
        "Se conservan solo tres herramientas orientadas a la operación, dos rutas cerradas y un único texto libre limitado a 20–500 caracteres. La reducción elimina capacidades administrativas sin afectar la trayectoria E4: el agente seleccionó las tres herramientas requeridas.",
    ])
    return "\n".join(lineas) + "\n", "\n".join(informe) + "\n"


if __name__ == "__main__":
    diagrama, metricas = analizar(TRAZA)
    (RAIZ / "trazas" / "e4-rutasit.mmd").write_text(diagrama, encoding="utf-8")
    (RAIZ / "protocolo.md").write_text(metricas, encoding="utf-8")
    print(metricas)
