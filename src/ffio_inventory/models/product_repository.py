import attrs
from sqlalchemy import select, insert, update, delete
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
    def add(self, product: Product) -> Product:
        with self.open_transaction() as connection:
            res = connection.execute(
                insert(product_table).values(
                    sku=product.sku,
                    name=product.name,
                    description=product.description,
                )
            )
            return attrs.evolve(product, id=res.inserted_primary_key[0])

    def update(self, product: Product) -> Product:
        with self.open_transaction() as connection:
            res = connection.execute(
                update(product_table)
                .where(product_table.c.id == product._id)
                .values(
                    sku=product.sku,
                    name=product.name,
                    description=product.description,
                )
            )

    def load(self, product_id: int) -> Product:
        with self.open_transaction() as connection:
            res = connection.execute(select(product_table).where(product_table.c.id == product_id))
        row = res.fetchone()
        if row is None:
            raise KeyError(f"Product ID {product_id} not found")
        return Product(**row)

    def load_all(self) -> list[Product]:
        with self.open_transaction() as connection:
            res = connection.execute(select(product_table))
        return [Product(**row) for row in res.fetchall()]

    def remove(self, product_id: int) -> None:
        with self.open_transaction() as connection:
            res = connection.execute(delete(product_table).where(product_table.c.id == product_id))
