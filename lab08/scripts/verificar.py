"""Ejecuta comprobaciones y conserva salidas reales; falla ante cualquier regresión."""

import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "lab08/evidencias"


def ejecutar(nombre, comando, cwd=ROOT, pythonpath=None):
    env = os.environ.copy()
    if pythonpath:
        env["PYTHONPATH"] = str(pythonpath)
    resultado = subprocess.run(comando, cwd=cwd, env=env, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    texto = "$ " + " ".join(comando) + "\n" + resultado.stdout + f"\nexit_code={resultado.returncode}\n"
    (OUT / nombre).write_text(texto)
    print(texto)
    resultado.check_returncode()


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    ejecutar("pytest.txt", [sys.executable, "-m", "pytest", "lab08/tests", "-v"])
    ejecutar("import-linter.txt", [str(Path(sys.executable).with_name("lint-imports")),
                                  "--config", ".importlinter", "--no-cache"])
    ejecutar("regresion-lab07.txt", [sys.executable, "-m", "pytest", "tests", "-q"],
             ROOT / "lab07", ROOT / "lab07/src")
    ejecutar("regresion-lab05.txt", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
             ROOT / "lab05", ROOT / "lab05/src")
