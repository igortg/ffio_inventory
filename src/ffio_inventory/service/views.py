from ffio_inventory.models.product import Product
from ffio_inventory.service.uow import UnitOfWork


def load_all_products(uow: UnitOfWork) -> list[Product]:
    with uow:
        return uow.products.load_all()
