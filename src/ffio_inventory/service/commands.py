import logging
from pathlib import Path

from ffio_inventory.models.product import Product
from ffio_inventory.service.uow import UnitOfWork

log = logging.getLogger(__name__)


def add_product(uow: UnitOfWork, product: Product) -> Product:
    with uow:
        return uow.products.add(product)


def update_product(uow: UnitOfWork, product: Product) -> Product:
    with uow:
        return uow.products.update(product)


def remove_product(uow: UnitOfWork, product: Product) -> Product:
    with uow:
        return uow.products.remove(product._id)


def load_products_from_csv(uow: UnitOfWork, csv_file_path: Path) -> None:
    """
    Load products from a CSV file with 3 columns: name,sku,description
    """
    with uow:
        products = []
        with csv_file_path.open() as csv_file:
            _ = csv_file.readline()  # skip file header
            for i, line in enumerate(csv_file):
                cells = line.strip().split(",")
                if not len(cells) or cells[0].strip() == '':
                    continue

                product = Product(
                    name=cells[0],
                    sku=cells[1] if len(cells) > 1 else None,
                    description=cells[2] if len(cells) > 2 else None,
                )
                products.append(product)
                if i > 0 and i % 100_000 == 0:
                    log.info(f"{i} lines processed")
                    uow.products.add_multiples(products)
                    products[:] = []
        if len(products):
            uow.products.add_multiples(products)
