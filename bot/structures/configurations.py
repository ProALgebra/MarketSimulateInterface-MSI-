import logging

from dataclasses import dataclass

from shared.settings import (PG_DB, PG_HOST, PG_PASSWORD, PG_PORT, PG_USERNAME)

from shared.settings import (REDIS_USER_DB, REDIS_FSM_DB, REDIS_MISC_DB, REDIS_HOST,
                             REDIS_PORT, REDIS_PASSWORD, REDIS_USER_NAME, REDIS_STATE_TTL,
                             REDIS_DATA_TTL)

from shared.settings import TELEGRAM_TOKEN

from sqlalchemy.engine import URL


@dataclass
class DatabaseConfig:
    """Database connection variables"""
    name: str = PG_DB
    user: str = PG_USERNAME
    passwd: str = PG_PASSWORD
    port: int = PG_PORT
    host: str = PG_HOST


@dataclass
class RedisConfig:
    """Redis connection variables"""
    user_db: str = REDIS_USER_DB
    fsm_db: str = REDIS_FSM_DB
    misc_db: str = REDIS_MISC_DB
    host: str = REDIS_HOST
    port: int = REDIS_PORT
    passwd: int = REDIS_PASSWORD
    username: int = REDIS_USER_NAME
    state_ttl: int = REDIS_STATE_TTL
    data_ttl: int = REDIS_DATA_TTL


@dataclass
class BotConfig:
    """Bot configuration"""
    token: str = TELEGRAM_TOKEN


@dataclass
class Configuration:
    """All in one configuration's class"""

    db = DatabaseConfig()
    redis = RedisConfig()
    bot = BotConfig()


conf = Configuration()
