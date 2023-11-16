# Инструкция по запуску проекта

Для локального запуска проекта потребуется установленный docker версии 19.03.0 + и docker compose.

### I Запуск файлового хранилища

В первую очередь нужно создать контейнер с Minio и выпустить пару Access Key и Secret Key в веб интерфейсе хранилища.

Запуск контейнера с Minio: 
_docker compose up file-storage -d_
В браузере по адресу localhost:9090 будет находится административный интерфейс интерфейс Minio.
Во вкладе Access Keys нужно нажать на **Create access key**, запомнить ключи и нажать **Create**

### II Конфигурационный файл
Ключи доступа к minio, как и другие настройки, нужно поместить в файл .env.dev и положить в корневой директории проекта.
Пример файла:

```
# Postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123
DB_HOST=database
DB_PORT=5432
POSTGRES_DB=postgres

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Telegram
TELEGRAM_TOKEN=<your_tg_token>

# PG Admin
PGADMIN_DEFAULT_EMAIL=example@example.com
PGADMIN_DEFAULT_PASSWORD=123321

# mq
MQ_HOST=mq


# minio s3 storage
S3_HOST=file-storage
S3_PORT=9000
S3_ACCESS_KEY=<your_access_key>
S3_SECRET_KEY=<your_secret_key>
```

### III Запуск остальных контейнеров

Теперь можно запустить остальные контейнеры командой
_docker compose up -d_

### IV Создание таблиц в базе данных

В качестве инструмента для миграций в базе данных на проекте используется alembic

В корне проекта нужно запустить команду _alembic upgrade head_, чтобы создать нужные таблицы

**На этом локальное разворачивание проекта завершено, он готов к использованию**


