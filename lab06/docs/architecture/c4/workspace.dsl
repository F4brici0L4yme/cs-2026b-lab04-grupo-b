workspace "RutaSIT Arequipa" "Modelo C4 del seguimiento en tiempo real de los buses del SIT de Arequipa (Laboratorio 06)." {

    !identifiers hierarchical

    model {
        pasajero = person "Pasajero" "Consulta la ubicación de los buses y su ETA para planificar su viaje."
        operador = person "Operador" "Supervisa la flota, recibe alertas de desvío y administra rutas y paraderos."

        rutasit = softwareSystem "RutaSIT Arequipa" "Seguimiento en tiempo real de los buses del SIT: ubicación, ETA y alertas de desvío." {
        }

        gps = softwareSystem "Rastreador GPS de los buses" "Rastreador a bordo de cada unidad; transmite latitud, longitud y hora por red móvil 3G/4G." "Externo"
        mapas = softwareSystem "Mapas abiertos (OSM)" "Servicio externo de mapas abiertos que provee los tiles y la geometría de referencia." "Externo"

        pasajero -> rutasit "Consulta la ubicación de los buses y su ETA"
        operador -> rutasit "Supervisa la flota y administra rutas y paraderos"
        gps -> rutasit "Transmite la posición de cada unidad cada 10 s" "HTTPS/JSON"
        rutasit -> mapas "Solicita tiles y geometría del mapa" "HTTPS"
    }

    views {
        systemContext rutasit "Contexto" "Nivel 1: RutaSIT, sus usuarios y los sistemas externos." {
            include *
            autolayout lr
        }

        styles {
            element "Person" {
                shape person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "Externo" {
                background #999999
                color #ffffff
            }
        }
    }
}
