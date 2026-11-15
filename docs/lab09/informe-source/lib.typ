#let table-border-width = 0.5pt
#let header-border-color = rgb("#808080")
#let tb-header-bg-color = rgb("#C8310E")

#import "components/page-header.typ": page-header
#import "components/basic-info-table.typ": basic-info-table

#let define(name, value) = {
  [#metadata((name: name, value: value)) <var_export>]
}

#let unsa-report(
  course_name: none,
  lab_title: none,
  lab_number: none,
  instructor_name: none,
  members: (),
  year: none,
  presentation_date: none,
  sem_code: none,
  presentation_hour: "11:59:00",
  ..custom_vars,
  body,
) = {
  // Export metadata for CLI
  define("course_name", course_name)
  define("lab_title", lab_title)
  define("lab_number", lab_number)
  define("instructor_name", instructor_name)
  define("members", members)

  let gen-time = datetime.today()
  let resolved-year = if year != none { year } else { gen-time.year() }
  let resolved-presentation-date = if presentation_date != none {
    presentation_date
  } else {
    gen-time.display("[day]/[month]/[year]")
  }
  let resolved-sem-code = if sem_code != none {
    sem_code
  } else {
    if gen-time.month() < 8 { "A" } else { "B" }
  }

  define("year", resolved-year)
  define("presentation_date", resolved-presentation-date)
  define("sem_code", resolved-sem-code)
  define("presentation_hour", presentation_hour)

  // Custom vars export
  for (name, value) in custom_vars.named() {
    define(name, value)
  }

  // Layout
  set text(font: "Lato")
  show heading.where(level: 1): set text(size: 10pt)
  show heading.where(level: 2): set text(size: 9pt)
  set list(indent: 1em, marker: "-")
  set enum(numbering: "1.")
  set image(width: 90%)
  set figure(supplement: [Figura])
  show image: set align(center)

  set page(
    paper: "a4",
    margin: (
      top: 6cm,
      bottom: 2.54cm,
      left: 1.9cm,
      right: 1.9cm,
    ),
    header: page-header(),
    header-ascent: 5%,
  )

  align(center)[#text(size: 13pt, weight: "bold")[INFORME DE LABORATORIO]]

  basic-info-table(
    course_name,
    lab_title,
    lab_number,
    resolved-year,
    resolved-sem-code,
    resolved-presentation-date,
    presentation_hour,
    members,
    instructor_name,
  )

  body
}
