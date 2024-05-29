workspace {
name "Сайт заказа услуг"
    description "Система взаимодействия между клиентом и заказчиком через сайт для реализации обмена услугами"
    !identifiers hierarchical

       model {
        properties { 
            structurizr.groupSeparator "/"
        }

        user = person "Пользователь" {
            description "Пользователь сайта заказа услуг"
        }

        order_service_system = softwareSystem "Система услуг и заказов" {
            description "Система для предоставления заказов / услуг"
            user_service = container "User Service" {
                description "Сервис для авторизации и управления пользователями"
                technology "REST API"
            }
            order_service_service = container "Chat Service" {
                description "Сервис для работы с заказами и услугами"
                technology "REST API"
            }

            group "Слой данных" {

                redis_cache = container "Redis Cache" {
                    description "Кеш Redis для ускорения поиска пользователей"
                    technology "Redis"
                    tags "cache"
                }
                postgres_database = container "PostgreSQL Database" {
                    description "База данных PostgreSQL с пользователями и услугами"
                    technology "PostgreSQL"
                    tags "database"
                }
                mongo_database = container "MongoDB Database" {
                    description "База данных MongoDB с историей заказов"
                    technology "MongoDB"
                    tags "database"
                }
            }

            user -> user_service "Регистрация и авторизация"
            user -> order_service_service "Создание и управление заказами, обработка услуг"

            order_service_service -> redis_cache "Получение последних заказов"
            user_service -> postgres_database "CRUD операции с пользователями, поиск"
            user_service -> order_service_service "Передача данных о пользователе после авторизации"

            order_service_service -> postgres_database "CRUD операции с заказами / услугами"
            order_service_service -> mongo_database "CRUD истории заказов"
            order_service_service -> user_service "Проверка авторизации пользователя при добавлении нового заказа или услуги"
        }

        deploymentEnvironment "Production" {
        deploymentNode "Order&Service Server" {
            containerInstance order_service_system.user_service
            containerInstance order_service_system.order_service_service
            properties {
                "cpu" "4"
                "ram" "128Gb"
                "hdd" "2Tb"
            }
        }

        deploymentNode "databases" {

            deploymentNode "Database Server 1" {
                containerInstance order_service_system.postgres_database
                properties {
                    "cpu" "4"
                    "ram" "128Gb"
                    "hdd" "2Tb"
                }
            }

            deploymentNode "Cache Server" {
                containerInstance order_service_system.redis_cache
                properties {
                    "cpu" "2"
                    "ram" "64Gb"
                    "hdd" "1Tb"
                }
            }

            deploymentNode "DocumentDB Server" {
                containerInstance order_service_system.mongo_database
                instances 4
                properties {
                    "cpu" "4"
                    "ram" "128Gb"
                    "hdd" "2Tb"
                }
            }
        }
    }
}


    views {
        themes default

        properties { 
            structurizr.tooltips true
        }


        !script groovy {
            workspace.views.createDefaultViews()
            workspace.views.views.findAll { it instanceof com.structurizr.view.ModelView }.each { it.enableAutomaticLayout() }
        }

        dynamic order_service_system "UC01" "Создание нового пользователя" {
            autoLayout
            user -> order_service_system.user_service "Создать нового пользователя (POST /users)"
            order_service_system.user_service -> order_service_system.postgres_database "Сохранить данные о пользователе"
        }

        dynamic order_service_system "UC02" "Поиск пользователя по логину" {
            autoLayout
            user -> order_service_system.user_service "Поиск пользователя (GET /users?login={login})"
            order_service_system.user_service -> order_service_system.postgres_database "Поиск в базе данных"
            order_service_system.postgres_database -> order_service_system.user_service "Вернуть данные пользователя"
        }

        dynamic order_service_system "UC03" "Поиск пользователя по маске имя и фамилии" {
            autoLayout
            user -> order_service_system.user_service "Поиск пользователя (GET /users?name={name}&surname={surname})"
            order_service_system.user_service -> order_service_system.postgres_database "Поиск в базе данных"
            order_service_system.postgres_database -> order_service_system.user_service "Вернуть данные пользователя"
        }

        dynamic order_service_system "UC04" "Создание услуги" {
            autoLayout
            user -> order_service_system.order_service_service "Создать заказ или услугу (POST /services)"
            order_service_system.order_service_service -> order_service_system.user_service "Проверить авторизацию пользователя"
            order_service_system.user_service -> order_service_system.order_service_service "Подтвердить авторизацию"
            order_service_system.order_service_service -> order_service_system.postgres_database "Сохранить данные о новой услуге"
        }

        dynamic order_service_system "UC05" "Получение списка услуг" {
            autoLayout
            user -> order_service_system.order_service_service "Получить список услуг (GET /services/)"
            order_service_system.order_service_service -> order_service_system.user_service "Проверить авторизацию пользователя"
            order_service_system.user_service -> order_service_system.order_service_service "Подтвердить авторизацию"
            order_service_system.order_service_service -> order_service_system.redis_cache "Проверить наличие последних услуг в кэше"
            order_service_system.redis_cache -> order_service_system.order_service_service "Вернуть последние услуги (если есть)"
            order_service_system.order_service_service -> order_service_system.mongo_database "Получить историю услуг (если нет в кэше)"
            order_service_system.mongo_database -> order_service_system.order_service_service "Вернуть последние услуги"
        }

        dynamic order_service_system "UC06" "Добавление услуг в заказ" {
            autoLayout
            user -> order_service_system.order_service_service "Создать заказ - добавив одну или несколько услуг (POST /orders)"
            order_service_system.order_service_service -> order_service_system.user_service "Проверить авторизацию пользователя"
            order_service_system.user_service -> order_service_system.order_service_service "Подтвердить авторизацию"
            order_service_system.order_service_service -> order_service_system.postgres_database "Сохранить данные о новом заказе"
        }

        dynamic order_service_system "UC07" "Получение заказа для пользователя" {
            autoLayout
            user -> order_service_system.order_service_service "Получить информацию о заказе (GET /orders/{order_id})"
            order_service_system.order_service_service -> order_service_system.user_service "Проверить авторизацию пользователя"
            order_service_system.user_service -> order_service_system.order_service_service "Подтвердить авторизацию"
            order_service_system.order_service_service -> order_service_system.mongo_database "Получить информацию о заказе"
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}
