"""E5: romper contratos en una rama de un repositorio temporal y revertir.

Solo se copia el paquete del Lab 08. El árbol de trabajo del usuario no se toca.
"""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    preferida = Path("/tmp/opencode")
    with tempfile.TemporaryDirectory(prefix="lab08-violacion-", dir=preferida if preferida.exists() else None) as tmp:
        cwd = Path(tmp)
        shutil.copytree(ROOT / "lab08/src/rutasit8", cwd / "src/rutasit8",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copy(ROOT / ".importlinter", cwd / ".importlinter")
        env = dict(os.environ, PYTHONPATH=str(cwd / "src"))
        log = ["E5 — rama temporal aislada, violaciones reales y restauración\n"]

        def run(args, esperado=0):
            r = subprocess.run(args, cwd=cwd, env=env, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log.append("$ " + " ".join(args) + "\n" + r.stdout + f"exit_code={r.returncode}\n")
            if r.returncode != esperado:
                raise RuntimeError("\n".join(log))
            return r.stdout

        run(["git", "init", "-b", "main"])
        run(["git", "add", "."])
        run(["git", "-c", "user.name=Prueba local Lab08", "-c", "user.email=lab08@example.invalid",
             "commit", "-m", "Base temporal para prueba estructural"])
        run(["git", "switch", "-c", "test/lab08-violaciones"])
        lint = [str(Path(sys.executable).with_name("lint-imports")), "--config", ".importlinter", "--no-cache"]
        assert "2 kept, 0 broken" in run(lint)
        casos = [("src/rutasit8/dominio.py", "\nfrom rutasit8.aplicacion import seguimiento\n", "1 broken"),
                 ("src/rutasit8/aplicacion/seguimiento.py",
                  "\nfrom rutasit8.infraestructura import memoria\n", "2 broken")]
        for archivo, importacion, esperado in casos:
            ruta = cwd / archivo
            ruta.write_text(ruta.read_text() + importacion)
            log.append(f"Violación introducida en {archivo}: {importacion.strip()}\n")
            assert esperado in run(lint, esperado=1)
            run(["git", "restore", archivo])
            assert "2 kept, 0 broken" in run(lint)
        run(["git", "status", "--short"])
        salida = ROOT / "lab08/evidencias/violaciones.txt"
        salida.write_text("\n".join(log))
        print(salida)


if __name__ == "__main__":
    main()
