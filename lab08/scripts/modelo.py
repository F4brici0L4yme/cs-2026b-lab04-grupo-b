"""Valida y exporta C4 usando la misma imagen por digest local y en CI."""

import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
C4 = ROOT / "lab08/docs/architecture/c4"
IMAGEN = "structurizr/structurizr@sha256:721136283c2f9cf1ba69037bc9de136c579d66fdcb2d771cb60546ec68def1a5"


def main():
    base = ["docker", "run", "--rm", "--user", f"{os.getuid()}:{os.getgid()}",
            "-v", f"{C4}:/usr/local/structurizr", IMAGEN]
    log = []
    for args in (["validate", "-w", "workspace.dsl"],
                 ["export", "-w", "workspace.dsl", "-f", "plantuml/c4plantuml", "-o", "export"],
                 ["export", "-w", "workspace.dsl", "-f", "mermaid", "-o", "export"]):
        comando = base + args
        r = subprocess.run(comando, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.append("$ " + " ".join(comando) + "\n" + r.stdout + f"\nexit_code={r.returncode}\n")
        print(r.stdout)
        (ROOT / "lab08/evidencias/structurizr.txt").write_text("\n".join(log))
        r.check_returncode()


if __name__ == "__main__":
    main()
