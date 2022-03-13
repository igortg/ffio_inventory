import pytest as pytest


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    return 'postgresql://postgres:masterkey@localhost:5432/ffio_inventory'
