from sqlalchemy import select, insert
from sqlalchemy.future import Connection
from sqlalchemy.util.compat import contextmanager

from ffio_inventory.models.product import Product
from ffio_inventory.models.schema import product_table


class BaseRepository:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    @contextmanager
    def open_transaction(self):
        with self._connection.begin() as trans:
            yield self._connection


class ProductRepository(BaseRepository):
    def add(self, product: Product) -> None:
        with self.open_transaction() as connection:
            res = connection.execute(
                insert(product_table).values(
                    sku=product.sku,
                    name=product.name,
                    description=product.description,
                )
            )

    def load(self, product_sku: str) -> Product:
        with self.open_transaction() as connection:
            res = connection.execute(
                select(product_table).where(product_table.c.sku == product_sku)
            )
        row = res.fetchone()
        if row is None:
            raise KeyError(f"Product for SKU '{product_sku}' not found")
        return Product(**row)
