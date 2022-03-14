from ffio_inventory.models.product import Product
from ffio_inventory.service.uow import UnitOfWork


def add_product(uow: UnitOfWork, product: Product) -> Product:
    with uow:
        return uow.products.add(product)


def update_product(uow: UnitOfWork, product: Product) -> Product:
    with uow:
        return uow.products.update(product)


def remove_product(uow: UnitOfWork, product: Product) -> Product:
    with uow:
        return uow.products.remove(product._id)
