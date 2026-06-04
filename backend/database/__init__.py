from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from backend.config import settings


@lru_cache
def get_engine():
    return create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)


@lru_cache
def get_session_factory():
    engine = get_engine()
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    factory = get_session_factory()
    async with factory() as session:
        yield session
