import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.engine import Engine

from ffio_inventory.api.app import create_app
from ffio_inventory.service.uow import UnitOfWork


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    return 'postgresql://postgres:masterkey@localhost:5432/ffio_inventory-test'


@pytest.fixture()
def flask_app(sqlalchemy_connect_url, create_tables) -> Flask:
    # TODO: create_tables is creating two engine objects
    app = create_app(sqlalchemy_connect_url)
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def api(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture()
def create_tables(engine: Engine):
    """
    Initialize the database for testing and drop all tables thereafter.

    Note: can be optimized later on by using nested transactions to avoid creating/dropping
    the entire database on each test.
    """
    from ffio_inventory.models.schema import metadata

    metadata.create_all(bind=engine)
    yield
    metadata.drop_all(bind=engine)


@pytest.fixture()
def uow(engine, create_tables):
    return UnitOfWork(engine)
