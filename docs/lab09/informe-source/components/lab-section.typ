#let default-align = left + top
#let default-stroke = black + 1pt
#let default-inset = 0.5em
#let default-header-fill = rgb("#C8310E")

#let lab-section(
  title: [],
  align-mode: none,
  stroke: none,
  inset: none,
  header-fill: none,
  body,
) = {
  let p_align_mode = if align-mode != none { align-mode } else { default-align }
  let p_stroke = if stroke != none { stroke } else { default-stroke }
  let p_inset = if inset != none { inset } else { default-inset }
  let p_header_fill = if header-fill != none { header-fill } else { default-header-fill }

  grid(
    align: p_align_mode,
    stroke: p_stroke,
    inset: p_inset,
    columns: 1fr,
    grid.header(
      repeat: false,
      [#grid.cell(fill: p_header_fill)[
        #set text(size: 11pt, weight: "bold", fill: white)
        #align(center)[#title]
      ]],
    ),
    [
      #set text(size: 8.5pt)
      #body
    ],
  )
}
