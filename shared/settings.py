from os import getenv

# Redis
REDIS_USER_DB: str = int(getenv("REDIS_USER_DATABASE", 1))
REDIS_FSM_DB: str = int(getenv("REDIS_FSM_DATABASE", 2))
REDIS_MISC_DB: str = int(getenv("REDIS_MISC_DATABASE", 3))
REDIS_HOST: str = getenv("REDIS_HOST", "localhost")
REDIS_PORT: int = int(getenv("REDIS_PORT", 6380))
REDIS_PASSWORD: int = getenv("REDIS_PASSWORD")
REDIS_USER_NAME: int = getenv("REDIS_USERNAME")
REDIS_STATE_TTL: int = getenv("REDIS_TTL_STATE", None)
REDIS_DATA_TTL: int = getenv("REDIS_TTL_DATA", None)

# Postgres
PG_USERNAME = getenv('POSTGRES_USER')
PG_PASSWORD = getenv('POSTGRES_PASSWORD')
PG_HOST = getenv('DB_HOST', default='127.0.0.1')
PG_PORT = int(getenv('DB_PORT', default=5432))
PG_DB = getenv('POSTGRES_DB')
PG_PROTOCOL = getenv('POSTGRES_PROTOCOL', default='postgresql+asyncpg')
PG_URI_QUERY = getenv('POSTGRES_URI_QUERY', default=str())

# rabbitmq
RABBITMQ_USERNAME = getenv('RABBIT_USER', default='guest')
RABBITMQ_PASSWORD = getenv('RABBIT_PASSWORD', default='guest')
RABBITMQ_HOST = getenv('RABBIT_HOST', default='127.0.0.1')
RABBITMQ_PORT = int(getenv('RABBIT_PORT', default=5672))
RABBITMQ_PROTOCOL = getenv('RABBIT_PROTOCOL', default='amqp')
RABBITMQ_URI_QUERY = getenv('RABBIT_URI_QUERY', default=str())

# Telegram
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')

# API key
API_KEY = getenv('API_KEY')