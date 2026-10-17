workspace "RutaSIT Arequipa" "Modelo C4 del seguimiento en tiempo real de los buses del SIT de Arequipa (Laboratorio 06)." {

    !identifiers hierarchical

    model {
        pasajero = person "Pasajero" "Consulta la ubicación de los buses y su ETA para planificar su viaje."
        operador = person "Operador" "Supervisa la flota, recibe alertas de desvío y administra rutas y paraderos."

        rutasit = softwareSystem "RutaSIT Arequipa" "Seguimiento en tiempo real de los buses del SIT: ubicación, ETA y alertas de desvío." {
            app = container "API RutaSIT" "Monolito modular (Ingesta, Flota, ETA, Alertas y Rutas) que expone la API REST de consulta, sirve el mapa del pasajero y el panel del operador." "Python 3.11 / Django" {
            }
            worker = container "Worker ETA/Alertas" "Procesa la telemetría de forma asíncrona: calcula el ETA y evalúa desvíos y alertas." "Celery"
            cache = container "Cola y caché" "Cola interna que desacopla la ingesta de posiciones y caché del estado reciente." "Redis" "Queue"
            db = container "Base de datos" "Rutas, paraderos, estado de flota, alertas e historial de 7 días; posiciones en tablas de series temporales (un esquema por módulo)." "PostgreSQL" "Database"
        }

        gps = softwareSystem "Rastreador GPS de los buses" "Rastreador a bordo de cada unidad; transmite latitud, longitud y hora por red móvil 3G/4G." "Externo"
        mapas = softwareSystem "Mapas abiertos (OSM)" "Servicio externo de mapas abiertos que provee los tiles y la geometría de referencia." "Externo"

        pasajero -> rutasit "Consulta la ubicación de los buses y su ETA"
        operador -> rutasit "Supervisa la flota y administra rutas y paraderos"
        gps -> rutasit "Transmite la posición de cada unidad cada 10 s" "HTTPS/JSON"
        rutasit -> mapas "Solicita tiles y geometría del mapa" "HTTPS"

        pasajero -> rutasit.app "Consulta la ubicación y el ETA de su bus" "HTTPS/JSON"
        operador -> rutasit.app "Consulta el panel de flota y el historial de alertas" "HTTPS/JSON"
        gps -> rutasit.app "Envía la posición de cada unidad cada 10 s" "HTTPS/JSON"
        rutasit.app -> rutasit.cache "Encola posiciones y alertas" "Redis protocol"
        rutasit.worker -> rutasit.cache "Consume posiciones y alertas" "Redis protocol"
        rutasit.app -> rutasit.db "Lee y escribe rutas, paraderos, estado y alertas" "SQL/TCP"
        rutasit.worker -> rutasit.db "Guarda posiciones, estado del bus y alertas" "SQL/TCP"
        rutasit.app -> mapas "Solicita tiles y geometría del mapa" "HTTPS"
    }

    views {
        systemContext rutasit "Contexto" "Nivel 1: RutaSIT, sus usuarios y los sistemas externos." {
            include *
            autolayout lr
        }

        container rutasit "Contenedores" "Nivel 2: contenedores del sistema y su tecnología." {
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
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Database" {
                shape cylinder
            }
            element "Queue" {
                shape pipe
            }
        }
    }
}
