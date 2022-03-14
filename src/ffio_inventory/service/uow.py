from sqlalchemy.engine import Engine, Connection, Transaction

from ffio_inventory.models.product_repository import ProductRepository


class UnitOfWork:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._connection: Connection | None = None
        self._trans: Transaction | None = None

        self._products: ProductRepository | None = None

    def __enter__(self) -> "UnitOfWork":
        self._connection = self._engine.connect()
        self._products = ProductRepository(self._connection)
        self._trans = self._connection.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self._trans.rollback()
        else:
            self._trans.commit()
        self._connection.close()

    @property
    def products(self):
        if self._products is None:
            raise UnitOfWorkError("Cannot access a repository out of a UnitOfWork context")
        return self._products


class UnitOfWorkError(Exception):
    """Raised when UnitOfWork is being misused"""
