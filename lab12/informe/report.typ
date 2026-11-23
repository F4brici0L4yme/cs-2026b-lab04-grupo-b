#import "lib.typ": unsa-report
#import "components/code-block.typ": code-block

#show: unsa-report.with(
  course_name: "Construcción de Software",
  lab_title: "Desarrollo asistido por IA: especificación, TDD y compuertas de calidad para RutaSIT",
  lab_number: "12",
  instructor_name: "Mg. Antonio Arroyo Paz",
  members: (
    "Layme Salas, Rodrigo Fabricio",
    "Auccacusi Conde, Brayan Carlos",
    "Castillo Lazo, Rodrigo Zarun",
  ),
  year: "2026",
  sem_code: "B",
  presentation_date: "28/11/2026",
)

#set image(width: 78%)
#set list(indent: 2pt)
#show raw.where(block: false): it => box(inset: (x: 0.5pt))[#it]

#include "sections/1-resultados.typ"
#v(0.5em)
#pagebreak()
#include "sections/2-cuestionario.typ"
#v(0.5em)
#pagebreak()
#include "sections/3-conclusiones.typ"
#v(0.5em)
#pagebreak()
#include "sections/4-referencias.typ"
