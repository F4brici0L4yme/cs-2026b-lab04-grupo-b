"""Renderiza fuentes Graphviz y exportaciones C4-PlantUML, sin editar el modelo."""

import argparse
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plantuml", required=True, type=Path, help="Ruta a plantuml-1.2025.2.jar")
    args = parser.parse_args()
    utilidad = BASE / "docs/architecture/utilidad"
    c4 = BASE / "docs/architecture/c4"
    (c4 / "img").mkdir(exist_ok=True)
    log = []
    comandos = [["dot", f"-T{fmt}", str(utilidad / "arbol.dot"), "-o", str(utilidad / f"arbol.{fmt}")]
                for fmt in ("png", "svg")]
    for fmt in ("png", "svg"):
        comandos.append(["java", "-DPLANTUML_LIMIT_SIZE=16384", "-jar", str(args.plantuml.resolve()),
                         "-failfast2", f"-t{fmt}", "-o", "../img",
                         *[str(p) for p in sorted((c4 / "export").glob("*.puml"))]])
    for comando in comandos:
        r = subprocess.run(comando, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.append("$ " + " ".join(comando) + "\n" + r.stdout + f"exit_code={r.returncode}\n")
        (BASE / "evidencias/diagramas.txt").write_text("\n".join(log))
        r.check_returncode()
    print("Árbol y cinco vistas C4 renderizados en PNG/SVG")


if __name__ == "__main__":
    main()
