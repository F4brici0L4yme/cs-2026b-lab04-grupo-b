#let cover-page(
  title: "",
  subtitle: none,
  logo-path: "/img/fixed/logo.png",
  course: "",
  teacher: "",
  authors: (),
  group: none,
  year: none,
  institution: (
    "UNIVERSIDAD NACIONAL DE SAN AGUSTÍN",
    "FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS",
    "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS"
  ),
  city-country: "AREQUIPA - PERÚ"
) = {
  align(center)[
    #for line in institution {
      strong(line)
      [\ ]
    }
    #v(3em)

    #if logo-path != none {
      image(logo-path, width: 5cm)
    }
    #v(2em)

    #strong("ACTIVIDAD PRÁCTICA") \
    #title
    #if subtitle != none [
      \ #subtitle
    ]
    #v(3em)

    #strong("ASIGNATURA") \
    #course
    #v(3em)

    #if group != none [
      #strong("GRUPO") \
      #group
      #v(3em)
    ]

    #strong("DOCENTE") \
    #teacher
    #v(3em)

    #let label = if authors.len() > 1 [INTEGRANTES] else [PRESENTADO POR]
    #strong(label) \
    #authors.join("\n")
    #v(3em)

    #strong(city-country) \
    #strong(if year != none { str(year) } else { "2026" })
  ]
}
