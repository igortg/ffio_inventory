from attrs import frozen


@frozen
class Product:
    sku: str
    name: str
    description: str = ""
