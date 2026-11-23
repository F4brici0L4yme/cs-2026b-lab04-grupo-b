#let __root = if "unsarep-root" in sys.inputs { sys.inputs.at("unsarep-root") } else { "/" }

#let default-prefix = "//"
#let default-lang = "text"
#let default-fill = rgb("#F1F3F4")
#let default-breakable = true
#let default-width = 100%
#let default-inset = 1em
#let default-radius = 8pt
#let default-spacing = 0.65em
#let default-clip = false
#let default-text-size = 7pt

#let extract-named-snippet(source, file, snippet-name, prefix) = {
  let lines = source.split("\n")
  let start-marker = prefix + " START-SNIPPET," + snippet-name
  let end-marker = prefix + " END-SNIPPET"
  let result = lines.fold((false, false, ()), (acc, line) => {
    let found-start = acc.at(0)
    let found-end = acc.at(1)
    let captured = acc.at(2)

    if found-end {
      acc
    } else if not found-start and line.trim() == start-marker {
      (true, false, ())
    } else if found-start and line.trim() == end-marker {
      (true, true, captured)
    } else if found-start {
      (true, false, captured + (line,))
    } else {
      acc
    }
  })

  if result.at(0) and result.at(1) {
    result.at(2).join("\n")
  } else {
    panic("Snippet '" + snippet-name + "' not found or not closed in file: " + file)
  }
}

#let code-block(
  file: none,
  snippet: none,
  prefix: none,
  lang: none,
  fill: none,
  breakable: none,
  width: none,
  inset: none,
  radius: none,
  spacing: none,
  clip: none,
  text-size: none,
) = {
  let p_prefix = if prefix != none { prefix } else { default-prefix }
  let p_lang = if lang != none { lang } else { default-lang }
  let p_fill = if fill != none { fill } else { default-fill }
  let p_breakable = if breakable != none { breakable } else { default-breakable }
  let p_width = if width != none { width } else { default-width }
  let p_inset = if inset != none { inset } else { default-inset }
  let p_radius = if radius != none { radius } else { default-radius }
  let p_spacing = if spacing != none { spacing } else { default-spacing }
  let p_clip = if clip != none { clip } else { default-clip }
  let p_text_size = if text-size != none { text-size } else { default-text-size }

  let source = read(__root + file)
  let code = if snippet == none {
    source
  } else {
    extract-named-snippet(source, file, snippet, p_prefix)
  }

  block(
    fill: p_fill,
    breakable: p_breakable,
    width: p_width,
    inset: p_inset,
    radius: p_radius,
    spacing: p_spacing,
    clip: p_clip,
  )[
    #set text(size: p_text_size)
    #set par(justify: false)
    #raw(code, lang: p_lang, block: true)
  ]
}
