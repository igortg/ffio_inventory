from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from ffio_inventory.models.schema import metadata

engine: Engine | None = None


def init_db(db_url: str):
    global engine
    engine = create_engine(db_url)
    metadata.create_all(bind=engine)


def acquire_engine() -> Engine:
    if engine is None:
        raise RuntimeError("init_db must be called first")
    return engine
