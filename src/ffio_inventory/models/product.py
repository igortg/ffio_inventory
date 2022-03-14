from attrs import frozen, field


@frozen
class Product:
    sku: str
    name: str
    description: str = ""
    _id: int | None = field(default=None, init=True)
