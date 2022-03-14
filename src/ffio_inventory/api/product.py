import attrs
from flask import request
from flask_restx import Resource, fields, Namespace

from ffio_inventory.models import db
from ffio_inventory.models.product import Product
from ffio_inventory.service import views, commands
from ffio_inventory.service.uow import UnitOfWork

ns = Namespace('products', description='Products operations', path="/product")

product_serializer = ns.model(
    'Product',
    {
        '_id': fields.Integer(required=True),
        'name': fields.String(required=True),
        'sku': fields.String(required=True),
        'description': fields.String(),
    },
)


@ns.route("")
class ProductList(Resource):
    @ns.marshal_with(product_serializer, code=201)
    def post(self):
        uow = UnitOfWork(db.engine)
        data = request.json
        new_product = Product(**data)
        new_product = commands.add_product(uow, new_product)
        return new_product, 201

    @ns.marshal_list_with(product_serializer)
    def get(self):
        uow = UnitOfWork(db.engine)
        products = views.load_all_products(uow)
        return [attrs.asdict(p) for p in products], 200
