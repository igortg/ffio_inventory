from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ffio_inventory.models.schema import metadata

engine = create_engine('postgresql://postgres:masterkey@localhost:5432/ffio_inventory')

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    metadata.create_all(bind=engine)
