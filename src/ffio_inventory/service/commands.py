import logging
import os
from pathlib import Path
from typing import Callable

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


def load_products_from_csv(
    uow: UnitOfWork, csv_file_path: Path, progress_callback: Callable[[str, int, int], None]
) -> None:
    """
    Load products from a CSV file with 3 columns: name,sku,description
    """
    with uow:
        products = []
        file_stat = os.stat(csv_file_path)
        file_size = file_stat.st_size
        file_pos = 0
        with csv_file_path.open("rb") as csv_file:
            header = csv_file.readline()  # skip file header
            file_pos += len(header)
            for i, line in enumerate(csv_file):
                file_pos += len(line)
                line = line.decode("utf8")
                cells = line.strip().split(",")
                if not len(cells) or cells[0].strip() == '':
                    continue

                product = Product(
                    name=cells[0],
                    sku=cells[1] if len(cells) > 1 else None,
                    description=cells[2] if len(cells) > 2 else None,
                )
                products.append(product)
                if i > 0 and i % 10_000 == 0:
                    progress_callback(f"{file_pos} of {file_size} read", file_pos, file_size)
                if i > 0 and i % 100_000 == 0:
                    log.info(f"{i} lines processed")
                    uow.products.add_multiples(products)
                    products[:] = []
        if len(products):
            uow.products.add_multiples(products)
