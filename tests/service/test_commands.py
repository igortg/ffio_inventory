import attrs

from ffio_inventory.models.product import Product
from ffio_inventory.service import commands, views


def test_crud_product(uow):
    prod1 = Product(sku="03542", name="Blue Shoe", description="Blue shoe with laces")

    prod1 = commands.add_product(uow, prod1)
    assert prod1._id is not None

    prod1 = attrs.evolve(prod1, description="Blue shoe with laces and heels")
    commands.update_product(uow, prod1)

    products = views.load_all_products(uow)
    assert products[0] == prod1

    commands.remove_product(uow, prod1)
    products = views.load_all_products(uow)
    assert len(products) == 0
