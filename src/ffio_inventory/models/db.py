from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from ffio_inventory.models.schema import metadata

engine: Engine | None = None


def init_db(db_url: str):
    global engine
    db_url = _fix_herokup_db_url(db_url)
    engine = create_engine(db_url, connect_args={'sslmode': 'require'})
    metadata.create_all(bind=engine)


def acquire_engine() -> Engine:
    if engine is None:
        raise RuntimeError("init_db must be called first")
    return engine


def _fix_herokup_db_url(db_url: str) -> str:
    """Heroku sets URL as 'postgres' but SQLAlchemy expects 'postgresql'"""
    return db_url.replace('postgres://', 'postgresql://')
