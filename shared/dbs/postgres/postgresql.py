from urllib.parse import urlunsplit

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from shared import settings


def get_pg_uri(
        username=settings.PG_USERNAME,
        password=settings.PG_PASSWORD,
        host=settings.PG_HOST,
        port=settings.PG_PORT,
        db=settings.PG_DB,
        protocol=settings.PG_PROTOCOL,
        uri_query=settings.PG_URI_QUERY
):
    return urlunsplit((protocol, f'{username}:{password}@{host}:{port}', db, uri_query, str()))


async_engine = create_async_engine(get_pg_uri())

async_session = async_sessionmaker(async_engine)
async_session_noauto = async_sessionmaker(async_engine, autocommit=False, autoflush=False, expire_on_commit=False)
