from dotenv import load_dotenv
from envparse import env

load_dotenv(env('DOTENV_FILE', default=None))

# Redis
REDIS_HOST = env('REDIS_HOST', default='127.0.0.1')
REDIS_DB = env('REDIS_DB')

# Postgres
PG_USERNAME = env('POSTGRES_USER')
PG_PASSWORD = env('POSTGRES_PASSWORD')
PG_HOST = env('DB_HOST', default='127.0.0.1')
PG_PORT = env.int('DB_PORT', default=5432)
PG_DB = env('POSTGRES_DB')
PG_PROTOCOL = env('POSTGRES_PROTOCOL', default='postgresql+asyncpg')
PG_URI_QUERY = env('POSTGRES_URI_QUERY', default=str())

# rabbitmq
RABBITMQ_USERNAME = env('RABBIT_USER', default='guest')
RABBITMQ_PASSWORD = env('RABBIT_PASSWORD', default='guest')
RABBITMQ_HOST = env('RABBIT_HOST', default='127.0.0.1')
RABBITMQ_PORT = env.int('RABBIT_PORT', default=5672)
RABBITMQ_PROTOCOL = env('RABBIT_PROTOCOL', default='amqp')
RABBITMQ_URI_QUERY = env('RABBIT_URI_QUERY', default=str())

# Telegram
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
