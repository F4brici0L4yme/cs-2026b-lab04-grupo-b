#!/usr/bin/env python3
"""Ejecuta las compuertas de calidad del hito HU-12."""
from __future__ import annotations

import os
import subprocess
import sys


def ejecutar(*comando: str, pythonpath: str | None = None) -> None:
    print("+", " ".join(comando), flush=True)
    entorno = os.environ.copy()
    if pythonpath:
        entorno["PYTHONPATH"] = pythonpath
    subprocess.run(comando, check=True, env=entorno)


def main() -> int:
    modulo = sys.argv[1] if len(sys.argv) > 1 else "hu-12"
    if modulo != "hu-12":
        print(f"Módulo no reconocido: {modulo}", file=sys.stderr)
        return 2
    ejecutar(sys.executable, "-m", "pytest", "--cov=rutasit_lab12", "-c", "lab12/pyproject.toml",
             "--cov-branch", "--cov-fail-under=85", "lab12/tests")
    ejecutar("ruff", "check", "lab12/src", "lab12/tests", "calidad")
    ejecutar("bandit", "-q", "-r", "lab12/src")
    ejecutar("radon", "cc", "-s", "-n", "C", "lab12/src")
    ejecutar(sys.executable, "-m", "pytest", "-q", "-c", "lab12/pyproject.toml", "-o", "pythonpath=../lab05/src", "lab05/tests")
    ejecutar(sys.executable, "-m", "pytest", "-q", "-c", "lab12/pyproject.toml", "-o", "pythonpath=../lab07/src", "lab07/tests")
    ejecutar(sys.executable, "-m", "pytest", "-q", "-c", "lab12/pyproject.toml", "-o",
             "pythonpath=../lab10/caso_rutasit/src", "lab10/tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
