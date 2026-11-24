"""Genera el informe del Lab 11 a partir de docs/informe.md y la plantilla UNSA.

Uso:
    .venv/bin/python scripts/generar_informe.py
    .venv/bin/python scripts/generar_informe.py --pdf

El Markdown es la fuente editable. El DOCX conserva el encabezado
institucional y la tabla de portada de la plantilla; las barras rojas y las
tablas se generan con el mismo estilo compacto de los informes anteriores.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from copy import deepcopy
from pathlib import Path

import markdown
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from lxml import html
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
FUENTE = BASE / "docs/informe.md"
PLANTILLA = BASE.parent / "como se hace" / "XX-CS-LAB PLANTILLA.docx"
DESTINO = BASE / "informe" / "Informe_Lab11_RutaSIT_MCP.docx"

ROJO = "C73514"
SECCIONES = (
    "SOLUCIÓN Y RESULTADOS",
    "SOLUCIÓN DEL CUESTIONARIO",
    "RETROALIMENTACIÓN GENERAL",
    "REFERENCIAS Y BIBLIOGRAFÍA",
)


def texto(elemento) -> str:
    return "".join(elemento.itertext()).strip()


def inline(parrafo, elemento) -> None:
    if elemento.text:
        parrafo.add_run(re.sub(r"\s+", " ", elemento.text))
    for hijo in elemento:
        run = parrafo.add_run(re.sub(r"\s+", " ", texto(hijo)))
        if hijo.tag in ("strong", "b"):
            run.bold = True
        elif hijo.tag in ("em", "i"):
            run.italic = True
        elif hijo.tag == "code":
            run.font.name = "Consolas"
            run.font.size = Pt(8.5)
        if hijo.tail:
            parrafo.add_run(re.sub(r"\s+", " ", hijo.tail))


def sombrear(celda, color: str) -> None:
    sombra = OxmlElement("w:shd")
    sombra.set(qn("w:fill"), color)
    celda._tc.get_or_add_tcPr().append(sombra)


def espaciar_celda(celda, arriba=80, abajo=80, lateral=100) -> None:
    celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    propiedades = celda._tc.get_or_add_tcPr()
    margenes = propiedades.first_child_found_in("w:tcMar")
    if margenes is None:
        margenes = OxmlElement("w:tcMar")
        propiedades.append(margenes)
    for lado, valor in (("top", arriba), ("bottom", abajo),
                        ("left", lateral), ("right", lateral)):
        nodo = margenes.find(qn(f"w:{lado}"))
        if nodo is None:
            nodo = OxmlElement(f"w:{lado}")
            margenes.append(nodo)
        nodo.set(qn("w:w"), str(valor))
        nodo.set(qn("w:type"), "dxa")


def separar_tabla(tabla) -> None:
    tabla.autofit = False
    propiedades = tabla._tbl.tblPr
    sangria = OxmlElement("w:tblInd")
    sangria.set(qn("w:w"), "283")
    sangria.set(qn("w:type"), "dxa")
    propiedades.append(sangria)
    for columna in tabla.columns:
        columna.width = Cm(16.1 / len(tabla.columns))


def ajustar_anchos(tabla) -> None:
    """Reparte el ancho disponible según el contenido de cada columna."""
    pesos = []
    for columna in tabla.columns:
        largo = max(len(celda.text.strip()) for celda in columna.cells) or 1
        pesos.append(max(4, min(70, largo)) ** 0.65)
    total = sum(pesos)
    anchos = [max(1.1, 16.1 * peso / total) for peso in pesos]
    for columna, ancho in zip(tabla.columns, anchos):
        columna.width = Cm(ancho)
        for celda in columna.cells:
            celda.width = Cm(ancho)


def barra(doc, titulo: str) -> None:
    tabla = doc.add_table(rows=1, cols=1)
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    separar_tabla(tabla)
    celda = tabla.cell(0, 0)
    espaciar_celda(celda, arriba=45, abajo=45)
    sombrear(celda, ROJO)
    parrafo = celda.paragraphs[0]
    parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    parrafo.paragraph_format.space_after = Pt(0)
    parrafo.paragraph_format.space_before = Pt(0)
    parrafo.paragraph_format.keep_with_next = True
    run = parrafo.add_run(titulo)
    run.bold = True
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(255, 255, 255)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def configurar(doc) -> None:
    normal = next(s for s in doc.styles if s.style_id == "Normal")
    normal.font.name = "Arial"
    normal.font.size = Pt(9.5)
    normal.paragraph_format.space_after = Pt(2.5)
    normal.paragraph_format.line_spacing = 1.06
    for nombre in ("Heading 1", "Heading 2", "Heading 3"):
        estilo = doc.styles[nombre]
        estilo.font.name = "Arial"
        estilo.font.size = Pt(10 if nombre == "Heading 3" else 11.5)
        estilo.font.bold = True
        estilo.font.color.rgb = RGBColor.from_string(ROJO)
        estilo.paragraph_format.space_before = Pt(7)
        estilo.paragraph_format.space_after = Pt(3)
        estilo.paragraph_format.keep_with_next = True
    if not any(s.name == "Table Grid" for s in doc.styles):
        doc.styles.element.append(deepcopy(Document().styles["Table Grid"].element))
    for seccion in doc.sections:
        seccion.page_width, seccion.page_height = Cm(21), Cm(29.7)
        seccion.left_margin = seccion.right_margin = Cm(1.85)
        seccion.top_margin, seccion.bottom_margin = Cm(3.2), Cm(1.25)


def portada(doc) -> None:
    tabla = doc.tables[0]
    tabla.cell(1, 1).text = "Construcción de Software"
    tabla.cell(2, 1).text = (
        "Protocolos y conectividad de contexto: diseñar, implementar, probar, "
        "conectar y auditar un servidor MCP — RutaSIT Arequipa"
    )
    tabla.cell(3, 1).text = "11"
    tabla.cell(3, 3).text = "2026-B"
    tabla.cell(3, 5).text = "VI"
    tabla.cell(4, 1).text = "28/11/2026 (fecha límite)"
    tabla.cell(4, 3).text = "23:59"
    tabla.cell(5, 0).text = (
        "INTEGRANTES:\nLayme Salas, Rodrigo Fabricio\n"
        "Auccacusi Conde, Brayan Carlos\nCastillo Lazo, Rodrigo Zarun"
    )
    tabla.cell(5, 5).text = "Reservado al docente"
    tabla.cell(6, 0).text = (
        "DOCENTES:\nMg. Antonio Arroyo Paz\nMg. Lino José Pinto Oppe\n"
        "Dr. Alexander Javier Benavides Rojas"
    )
    for fila in tabla.rows:
        for celda in fila.cells:
            for parrafo in celda.paragraphs:
                for run in parrafo.runs:
                    run.font.name, run.font.size = "Arial", Pt(9)
    encontrado = False
    for hijo in list(doc._element.body):
        if hijo is tabla._element:
            encontrado = True
        elif encontrado and hijo.tag != qn("w:sectPr"):
            doc._element.body.remove(hijo)
    doc.add_page_break()


def agregar_tabla(doc, nodo) -> None:
    filas = nodo.xpath(".//tr")
    if not filas:
        return
    tabla = doc.add_table(rows=0, cols=len(filas[0]))
    tabla.style = "Table Grid"
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    separar_tabla(tabla)
    for i, fila in enumerate(filas):
        celdas = tabla.add_row().cells
        tabla.rows[-1]._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for celda, valor in zip(celdas, fila):
            espaciar_celda(celda)
            inline(celda.paragraphs[0], valor)
            for parrafo in celda.paragraphs:
                for run in parrafo.runs:
                    run.font.size = Pt(7.8)
                    if i == 0:
                        run.bold = True
            if i == 0:
                sombrear(celda, ROJO)
                for run in celda.paragraphs[0].runs:
                    run.font.color.rgb = RGBColor(255, 255, 255)
            elif i % 2 == 0:
                sombrear(celda, "F4F4F4")
    if filas:
        tabla.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    ajustar_anchos(tabla)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def agregar_imagen(doc, nodo) -> None:
    imagen = nodo.find("img")
    if imagen is None:
        return
    ruta = (FUENTE.parent / imagen.get("src")).resolve()
    if not ruta.exists():
        raise FileNotFoundError(ruta)
    with Image.open(ruta) as im:
        ancho, alto = im.size
    ancho_cm = min(15.8, 13.5 * ancho / alto)
    parrafo = doc.add_paragraph()
    parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    parrafo.paragraph_format.keep_with_next = True
    parrafo.paragraph_format.space_before = Pt(4)
    parrafo.add_run().add_picture(str(ruta), width=Cm(ancho_cm))
    caption = doc.add_paragraph(imagen.get("alt", "Figura"))
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.paragraph_format.space_after = Pt(6)
    for run in caption.runs:
        run.italic = True
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor.from_string("555555")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plantilla", type=Path, default=PLANTILLA)
    parser.add_argument("--pdf", action="store_true", help="convierte el DOCX con LibreOffice")
    args = parser.parse_args()

    if not args.plantilla.exists():
        raise FileNotFoundError(args.plantilla)

    doc = Document(args.plantilla)
    portada(doc)
    configurar(doc)
    arbol = html.fragment_fromstring(
        markdown.markdown(FUENTE.read_text(encoding="utf-8"),
                          extensions=["tables", "fenced_code"]),
        create_parent="div",
    )

    empezado = False
    for nodo in arbol:
        if not empezado:
            if nodo.tag == "h2" and texto(nodo) == "Resumen":
                empezado = True
                barra(doc, "SOLUCIÓN Y RESULTADOS")
                doc.add_heading("RESUMEN", level=2)
            continue
        if nodo.tag in ("h1", "h2", "h3", "h4"):
            titulo = texto(nodo)
            if nodo.tag == "h2" and titulo.startswith(("I. ", "II. ", "III. ", "IV. ")):
                if titulo.startswith("I. "):
                    continue
                if titulo.startswith("II. "):
                    doc.add_page_break()
                    barra(doc, "SOLUCIÓN DEL CUESTIONARIO")
                elif titulo.startswith("III. "):
                    doc.add_page_break()
                    barra(doc, "RETROALIMENTACIÓN GENERAL")
                else:
                    barra(doc, "REFERENCIAS Y BIBLIOGRAFÍA")
            else:
                doc.add_heading(titulo, level=min(int(nodo.tag[1]), 3))
        elif nodo.tag == "table":
            agregar_tabla(doc, nodo)
        elif nodo.tag == "p" and nodo.find("img") is not None:
            agregar_imagen(doc, nodo)
        elif nodo.tag in ("ul", "ol"):
            for n, item in enumerate(nodo, 1):
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.5)
                p.add_run(f"{n}. " if nodo.tag == "ol" else "• ")
                inline(p, item)
        elif nodo.tag == "pre":
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.3)
            run = p.add_run(texto(nodo))
            run.font.name, run.font.size = "Consolas", Pt(8)
        elif nodo.tag == "blockquote":
            p = doc.add_paragraph()
            inline(p, nodo)
            for run in p.runs:
                run.italic = True
        else:
            inline(doc.add_paragraph(), nodo)

    if not empezado:
        raise ValueError("El informe debe comenzar con '## Resumen'")

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    doc.save(DESTINO)
    print(DESTINO)

    if args.pdf:
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir",
             str(DESTINO.parent), str(DESTINO)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(DESTINO.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
