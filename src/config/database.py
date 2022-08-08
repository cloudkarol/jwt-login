from sqlalchemy import create_engine, orm

from src.config import settings


def create_session(url: str) -> orm.scoped_session:
    engine = create_engine(
        url, pool_pre_ping=True, future=True,
    )
    factory = orm.sessionmaker(
        engine, autoflush=False, expire_on_commit=False,
    )
    return orm.scoped_session(factory)


session = create_session(settings.DATABASE_URI.replace('+asyncpg', ''))