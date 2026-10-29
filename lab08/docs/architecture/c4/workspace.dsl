workspace "RutaSIT Arequipa — Lab 08" "Evolución del workspace del Lab 06: tres iteraciones ADD, ADR-006 a ADR-008. Diseño objetivo; prototipo local en memoria." {
    !identifiers hierarchical
    model {
        pasajero = person "Pasajero" "Consulta ubicación y ETA; recibe estado textual si fallan mapas. [QA-02, QA-04, QA-07]"
        operador = person "Operador" "Supervisa flota y administra rutas; cambios versionan geometría. [QA-01, QA-03]"
        rutasit = softwareSystem "RutaSIT Arequipa" "Seguimiento de 1200 buses; 50 000 consultas en hora punta. Un VPS, monolito modular. [QA-01, QA-02, QA-03, QA-04, QA-05, QA-06, QA-07]" {
            app = container "API RutaSIT" "REST de ingesta/consulta y vista textual degradada. Lee ETA materializado, comprueba captura <=30 s y usa breaker de mapas. [QA-01, QA-02, QA-04, QA-05, QA-07]" "Python / Django" {
                presentacion = component "Presentación" "DTO público de unidad y estado textual con aviso de degradación. [QA-02, QA-05, QA-07]" "Python / Django"
                aplicacion = component "Aplicación" "Consulta ETA por puertos; comprueba vigencia, independiente del proveedor de mapas. [QA-04, QA-06, QA-07]" "Python"
                dominio = component "Dominio" "Reglas de unidad y lectura GPS; no rejuvenece fuente obsoleta. [QA-05, QA-07]" "Python"
                infraestructura = component "Infraestructura" "Read model, caché TTL <=2 s, adaptadores y breaker de mapas (3 fallas / 30 s). [QA-02, QA-04, QA-07]" "Python"
                compartido = component "Compartido" "Identificadores de unidad y tipos comunes, sin datos personales. [QA-05, QA-06]" "Python"
            }
            worker = container "Worker ETA/Alertas" "Procesa 120 eventos/s como objetivo; geometría precargada por versión, Strategy ETA, ID estable. [QA-01, QA-03, QA-06, QA-07]" "Celery"
            cache = container "Cola y caché" "Cola con AOF según ADR-003; caché ETA por bus/paradero, TTL <=2 s y memoria acotada. [QA-01, QA-03, QA-04, QA-07]" "Redis" "Queue"
            db = container "Base de datos" "Esquemas por módulo, historial y último ETA con clave compuesta bus/paradero y captura original. [QA-01, QA-03, QA-04, QA-05, QA-07]" "PostgreSQL" "Database"
        }
        gps = softwareSystem "Rastreador GPS de los buses" "1200 unidades transmiten posición cada 10 s e ID estable. [QA-01, QA-03, QA-07]" "Externo"
        mapas = softwareSystem "Mapas abiertos (OSM)" "Proveedor externo de tiles y geometría; su caída no elimina estado textual. [QA-02]" "Externo"
        pasajero -> rutasit "Consulta ubicación y ETA; recibe aviso si hay degradación"
        operador -> rutasit "Supervisa flota y versiona rutas/paraderos"
        gps -> rutasit "Envía posición cada 10 s" "HTTPS/JSON"
        rutasit -> mapas "Solicita mapa con protección ante fallas" "HTTPS"
        pasajero -> rutasit.app "Consulta ETA y estado" "HTTPS/JSON"
        operador -> rutasit.app "Consulta panel y configura rutas" "HTTPS/JSON"
        gps -> rutasit.app "Envía posición e ID estable" "HTTPS/JSON"
        rutasit.app -> rutasit.cache "Encola posiciones; lee caché ETA TTL <=2 s" "Redis protocol"
        rutasit.worker -> rutasit.cache "Consume posiciones y publica ETA reciente" "Redis protocol"
        rutasit.app -> rutasit.db "Lee último ETA por clave; administra rutas" "SQL/TCP"
        rutasit.worker -> rutasit.db "Lee geometría por versión; guarda historial y último ETA" "SQL/TCP"
        rutasit.app -> mapas "Solicita mapa: breaker 3 fallas, sondeo 30 s [QA-02]" "HTTPS"
        rutasit.app.presentacion -> rutasit.app.aplicacion "Invoca consulta de seguimiento"
        rutasit.app.aplicacion -> rutasit.app.dominio "Verifica vigencia de la captura"
        rutasit.app.aplicacion -> rutasit.app.compartido "Usa identificadores de unidad"
        rutasit.app.dominio -> rutasit.app.compartido "Usa tipos comunes"
        rutasit.app.infraestructura -> rutasit.app.aplicacion "Implementa puertos; composición en arranque"
        rutasit.app.infraestructura -> rutasit.app.dominio "Reconstruye lecturas sin rejuvenecerlas"
        rutasit.app.infraestructura -> rutasit.cache "Lee caché ETA de corto plazo" "Redis protocol"
        rutasit.app.infraestructura -> rutasit.db "Consulta read model por bus/paradero" "SQL/TCP"
        rutasit.app.infraestructura -> mapas "Adapta mapas con circuit breaker" "HTTPS"
        pasajero -> rutasit.app.presentacion "Solicita seguimiento" "HTTPS/JSON"
        operador -> rutasit.app.presentacion "Consulta panel" "HTTPS/JSON"
        gps -> rutasit.app.presentacion "Envía posición" "HTTPS/JSON"
        produccion = deploymentEnvironment "Producción" {
            deploymentNode "Bus del SIT (1200 unidades)" "Objetivo de crecimiento de la guía 08. [QA-01, QA-03]" "Red móvil 3G/4G" {
                deploymentNode "Rastreador GPS" "Posición cada 10 s; timestamp de captura. [QA-01, QA-07]" "Unidad a bordo" {
                    softwareSystemInstance gps
                }
            }
            deploymentNode "VPS único (R-03)" "Diseño heredado del Lab 06; CPU <70% aún no medido. [QA-01, QA-03, QA-04]" "Ubuntu 24.04 LTS / 2 vCPU / 4 GB RAM" {
                containerInstance rutasit.app
                containerInstance rutasit.worker
                containerInstance rutasit.cache
                containerInstance rutasit.db
            }
        }
    }
    views {
        systemContext rutasit "Contexto" "Sistema, actores y dependencias externas [QA-01..07]." {
            include *
            autolayout lr
        }
        container rutasit "Contenedores" "E6: contenedores después de las tres iteraciones ADD." {
            include *
            autolayout lr
        }
        component rutasit.app "Componentes" "Capas del Lab 05 refinadas con puertos, caché y resiliencia." {
            include *
            autolayout lr
        }
        dynamic rutasit "ActualizacionETA" "Captura GPS y actualización de ETA, conservando timestamp [QA-01, QA-07]." {
            gps -> rutasit.app "Envía posición con ID estable y timestamp"
            rutasit.app -> rutasit.cache "Valida y encola posición"
            rutasit.worker -> rutasit.cache "Consume posición"
            rutasit.worker -> rutasit.db "Usa geometría vigente y guarda ETA materializado"
            rutasit.worker -> rutasit.cache "Publica lectura reciente"
            pasajero -> rutasit.app "Consulta bus/paradero"
            rutasit.app -> rutasit.cache "Lee ETA y comprueba captura <=30 s"
            autolayout lr
        }
        deployment rutasit produccion "Despliegue" "Un VPS; cuatro contenedores no equivalen a microservicios." {
            include *
            autolayout lr
        }
        styles {
            element "Person" {
                shape person
                background #08427b
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Externo" {
                background #777777
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Component" {
                background #85bbf0
                color #000000
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
