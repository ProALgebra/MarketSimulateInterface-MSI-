from typing import Any, Optional, TypeVar, final

from aioredis.client import Redis, ExpiryT

from bot.structures import conf

KeyLike = TypeVar("KeyLike", str, int)


class Adapter:
    """Cache adapter"""
    def __init__(self,
                 host: str,
                 db: str,
                 port: int,
                 password: str,
                 username: str):
        self.client = self.build_redis_client(host, db, port, password, username)

    @staticmethod
    def build_redis_client(
            host: str,
            db: str,
            port: int,
            password: str,
            username: str,
    ) -> Redis:
        """Build redis client
        :param username: username
        :param port: port database
        :param db: number database
        :param host: host database
        :type password: password database
        """
        client = Redis(
            host=host,
            db=db,
            port=port,
            password=password,
            username=username,
        )
        return client

    @property
    def redis_client(self) -> Redis:
        """
        Redis client which used in the cache adapter
        :return:
        """
        return self.client

    @final
    async def get(self, key: KeyLike) -> Any:
        """
        Get a value from cache database
        :param key:
        :return: Value
        """
        return await self.client.get(str(key))

    @final
    async def set(self, key: KeyLike, value: Any, expire: Optional[ExpiryT] = None):
        """
        Set a value to cache database
        :param expire: Time to delete key in seconds
        :param key: Key to set
        :param value: Value in a serializable type
        :return: Nothing
        """
        await self.client.set(name=str(key), value=value, ex=expire)

    @final
    async def lpush(self, key: KeyLike, value: Any, expire: Optional[ExpiryT] = None):
        """
        Set a value to cache database
        :param expire: Time to delete key in seconds
        :param key: Key to set
        :param value: Value in a serializable type
        :return: Nothing
        """
        await self.client.lpush(name=str(key), value=value, ex=expire)

    @final
    async def exists(self, key: KeyLike) -> bool:
        """
        Check whether key has already defined or not
        :param key:
        :return: (bool) Result
        """
        return await self.client.exists(str(key))

    @final
    async def delete(self, key: KeyLike) -> bool:
        """
        Delete one or more keys specified by ``names``
        :param key:
        :return: (bool) Result
        """
        return await self.client.delete(str(key))


class Cache:
    """ A class for interacting with different Redis database spaces """
    user_client: Adapter = Adapter(conf.redis.host,
                                   conf.redis.user_db,
                                   conf.redis.port,
                                   conf.redis.passwd,
                                   conf.redis.username)

    fsm_client: Adapter = Adapter(conf.redis.host,
                                  conf.redis.fsm_db,
                                  conf.redis.port,
                                  conf.redis.passwd,
                                  conf.redis.username)

    misc_client: Adapter = Adapter(conf.redis.host,
                                   conf.redis.misc_db,
                                   conf.redis.port,
                                   conf.redis.passwd,
                                   conf.redis.username)

    async def close(self):
        await self.user_client.client.close()
        await self.fsm_client.client.close()
        await self.misc_client.client.close()
