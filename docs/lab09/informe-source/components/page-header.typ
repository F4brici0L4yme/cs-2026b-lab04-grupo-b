#let default-border-width = 0.5pt
#let default-border-color = rgb("#808080")

#let page-header() = block(
  width: 100%,
  inset: (bottom: 1em),
)[
  #table(
    align: center + horizon,
    stroke: default-border-width + default-border-color,
    columns: (1fr, 2fr, 1fr),
    align(horizon)[#image("/img/fixed/epis.png", width: 95%)],
    table.cell(align: center + horizon)[
      #set text(size: 7.5pt, weight: "bold")
      UNIVERSIDAD NACIONAL DE SAN AGUSTÍN \
      FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS \
      ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS
    ],
    align(horizon)[#image("/img/fixed/abet.png", width: 97%)],
    table.cell(colspan: 3)[
      #set text(size: 7pt)
      #text(weight: "bold")[Formato: ]
      Guía de Práctica de Laboratorio / Talleres / Centros de Simulación
    ],
    table.cell[
      #set text(size: 7pt, weight: "bold")
      Aprobación: 2022/03/01
    ],
    table.cell[
      #set text(size: 7pt, weight: "bold")
      Código: GUIA-PRLE-001
    ],
    context table.cell(align: right + horizon)[
      #set text(size: 7pt, weight: "bold")
      Página: #counter(page).display("1")
    ],
  )
]
