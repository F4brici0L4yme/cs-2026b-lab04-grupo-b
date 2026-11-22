"""Herramientas de lectura, edición exacta y ejecución sin shell."""

from __future__ import annotations

import ast
import shlex
import subprocess
from pathlib import Path


class Herramientas:
    def __init__(self, raiz: Path, limite_salida: int = 600):
        self.raiz = raiz.resolve()
        self.limite_salida = limite_salida
        self.archivo_notas = self._ruta("agentes/notas.md")

    def catalogo(self) -> dict[str, str]:
        return {
            "listar_archivos": "Lista archivos relativos bajo una ruta.",
            "leer_archivo": "Lee un archivo de texto dentro del repositorio.",
            "buscar": "Busca una cadena literal en archivos de texto.",
            "mapa_repo": "Resume módulos, clases y firmas mediante el AST de Python.",
            "editar_archivo": "Reemplaza exactamente una ocurrencia en un archivo permitido.",
            "ejecutar_comando": "Ejecuta un comando de la lista permitida, sin shell.",
            "ver_cambios": "Muestra estado y resumen del diff de Git.",
            "anotar": "Añade una nota de trabajo al archivo de memoria del agente.",
            "leer_notas": "Lee las notas guardadas por el agente.",
        }

    def _ruta(self, ruta: str) -> Path:
        destino = (self.raiz / ruta).resolve()
        if self.raiz not in destino.parents and destino != self.raiz:
            raise PermissionError(f"Ruta fuera del sandbox: {ruta}")
        return destino

    def listar_archivos(self, ruta: str = ".") -> str:
        base = self._ruta(ruta)
        if not base.is_dir():
            return f"ERROR: no es un directorio: {ruta}"
        excluidos = {".git", ".venv", "__pycache__"}
        resultados = [
            p.relative_to(self.raiz).as_posix()
            for p in sorted(base.rglob("*"))
            if p.is_file() and not any(parte in excluidos for parte in p.parts)
        ]
        return "\n".join(resultados[:200]) or "(directorio vacío)"

    def leer_archivo(self, ruta: str) -> str:
        archivo = self._ruta(ruta)
        if not archivo.is_file():
            return f"ERROR: no existe: {ruta}"
        contenido = archivo.read_text(encoding="utf-8")
        return contenido[:12000] + ("\n[contenido truncado]" if len(contenido) > 12000 else "")

    def buscar(self, texto: str, ruta: str = ".") -> str:
        base = self._ruta(ruta)
        resultados: list[str] = []
        for archivo in sorted(base.rglob("*")):
            if not archivo.is_file() or archivo.suffix not in {".py", ".md", ".json", ".mmd", ".puml"}:
                continue
            if any(p in {".git", ".venv", "__pycache__"} for p in archivo.parts):
                continue
            try:
                for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                    if texto in linea:
                        resultados.append(
                            f"{archivo.relative_to(self.raiz).as_posix()}:{numero}: {linea[:220]}"
                        )
            except UnicodeDecodeError:
                continue
        return "\n".join(resultados[:40]) or "(sin coincidencias)"

    def mapa_repo(self, ruta: str = "lab10/caso_rutasit/src") -> str:
        base = self._ruta(ruta)
        if not base.is_dir():
            return f"ERROR: no es un directorio: {ruta}"
        resultados: list[str] = []
        for archivo in sorted(base.rglob("*.py")):
            try:
                arbol = ast.parse(archivo.read_text(encoding="utf-8"))
            except (OSError, SyntaxError, UnicodeDecodeError) as error:
                resultados.append(
                    f"{archivo.relative_to(self.raiz).as_posix()}: ERROR {type(error).__name__}"
                )
                continue
            relativo = archivo.relative_to(self.raiz).as_posix()
            resultados.append(f"{relativo}:")
            for nodo in arbol.body:
                if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    resultados.append(f"  def {nodo.name}({ast.unparse(nodo.args)})")
                elif isinstance(nodo, ast.ClassDef):
                    resultados.append(f"  class {nodo.name}")
                    for miembro in nodo.body:
                        if isinstance(miembro, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            resultados.append(
                                f"    def {miembro.name}({ast.unparse(miembro.args)})"
                            )
        return "\n".join(resultados[:200]) or "(no se encontraron fuentes Python)"

    def editar_archivo(self, ruta: str, antes: str, despues: str) -> str:
        archivo = self._ruta(ruta)
        if not archivo.is_file():
            return f"ERROR: no existe: {ruta}"
        if not antes:
            return "ERROR: el texto de búsqueda no puede estar vacío"
        contenido = archivo.read_text(encoding="utf-8")
        ocurrencias = contenido.count(antes)
        if ocurrencias != 1:
            return f"ERROR: el fragmento aparece {ocurrencias} veces; debe aparecer exactamente 1"
        archivo.write_text(contenido.replace(antes, despues), encoding="utf-8")
        return f"OK: {ruta} modificado"

    def ejecutar_comando(self, comando: str) -> str:
        argumentos = shlex.split(comando)
        if not argumentos:
            return "ERROR: comando vacío"
        resultado = subprocess.run(
            argumentos,
            cwd=self.raiz,
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        salida = (resultado.stdout + resultado.stderr).strip()
        if not salida:
            salida = "(sin salida)"
        return f"código={resultado.returncode}\n{salida[:self.limite_salida]}"

    def ver_cambios(self) -> str:
        estado = self.ejecutar_comando("git status --short")
        diff = self.ejecutar_comando("git diff --stat")
        return f"ESTADO\n{estado}\nDIFF\n{diff}"

    def anotar(self, texto: str) -> str:
        if not texto.strip() or len(texto) > 500:
            return "ERROR: la nota debe tener entre 1 y 500 caracteres"
        self.archivo_notas.parent.mkdir(parents=True, exist_ok=True)
        linea = f"- {texto.strip()}"
        if self.archivo_notas.exists() and linea in self.archivo_notas.read_text(
            encoding="utf-8"
        ).splitlines():
            return "OK: nota ya registrada"
        with self.archivo_notas.open("a", encoding="utf-8") as archivo:
            archivo.write(f"{linea}\n")
        return "OK: nota guardada"

    def leer_notas(self) -> str:
        if not self.archivo_notas.exists():
            return "(todavía no hay notas)"
        return self.archivo_notas.read_text(encoding="utf-8")[:4000]
