import pytest
from _pytest.fixtures import FixtureRequest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.engine import Engine

from ffio_inventory.api.app import create_app
from ffio_inventory.service.uow import UnitOfWork


@pytest.fixture()
def flask_app() -> Flask:
    app = create_app()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def api(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    return 'postgresql://postgres:masterkey@localhost:5432/ffio_inventory'


@pytest.fixture(scope="session")
def create_tables(engine: Engine, request: FixtureRequest):
    from ffio_inventory.models.schema import metadata

    def finalizer():
        metadata.drop_all(bind=engine)

    request.addfinalizer(finalizer)
    metadata.create_all(bind=engine)


@pytest.fixture()
def uow(engine, create_tables):
    return UnitOfWork(engine)
