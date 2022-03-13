import pytest
from sqlalchemy.engine import Connection

from ffio_inventory.models.product import Product
from ffio_inventory.models.product_repository import ProductRepository


def test_crud(connection: Connection) -> None:
    sample = Product(name="Mi A3", sku="mia3")

    repo = ProductRepository(connection)
    repo.add(sample)
    repo.load("mia3")


def test_sku_not_found(connection: Connection) -> None:
    repo = ProductRepository(connection)
    with pytest.raises(KeyError):
        repo.load("not_found")
