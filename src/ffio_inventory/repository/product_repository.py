import attrs
from sqlalchemy import select, insert, update, delete, text
from sqlalchemy.future import Connection
from sqlalchemy.util.compat import contextmanager

from ffio_inventory.models.product import Product
from ffio_inventory.repository.schema import product_table


class BaseRepository:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    @contextmanager
    def open_transaction(self):
        with self._connection.begin():
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

    def add_multiples(self, product_list: list[Product]) -> None:
        """
        Add a list of products, updating duplicates when it's the case.
        """
        s = text(
            f"""
        INSERT INTO {product_table.name} (
            {product_table.c.sku.name},
            {product_table.c.name.name},
            {product_table.c.description.name}
            ) 
        VALUES (:sku, :name, :description)
        ON CONFLICT ({product_table.c.sku.name}) DO UPDATE
        SET
            {product_table.c.name.name} = :name,
            {product_table.c.description.name} = :description
        """
        )
        rows = [{'sku': p.sku, 'name': p.name, 'description': p.description} for p in product_list]
        with self.open_transaction() as connection:
            connection.execute(s, rows)

    def update(self, product: Product) -> None:
        with self.open_transaction() as connection:
            # noinspection PyProtectedMember
            connection.execute(
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

    def load_all(self, *, limit: int = 50) -> list[Product]:
        with self.open_transaction() as connection:
            res = connection.execute(select(product_table).limit(limit))
        return [Product(**row) for row in res.fetchall()]

    def remove(self, product_id: int) -> None:
        with self.open_transaction() as connection:
            connection.execute(delete(product_table).where(product_table.c.id == product_id))
