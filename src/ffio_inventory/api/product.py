import attrs
from flask import request, current_app
from flask_restx import Resource, fields, Namespace

from ffio_inventory.core import UPLOAD_FOLDER
from ffio_inventory.models.product import Product
from ffio_inventory.repository import db
from ffio_inventory.service import views, commands
from ffio_inventory.service.uow import UnitOfWork
from ffio_inventory.worker import tasks

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
class ProductListEndpoint(Resource):
    @ns.marshal_with(product_serializer, code=201)
    def post(self):
        uow = UnitOfWork(db.engine)
        data = request.json
        new_product = Product(**data)
        new_product = commands.add_product(uow, new_product)
        return new_product

    @ns.marshal_list_with(product_serializer)
    def get(self):
        uow = UnitOfWork(db.engine)
        products = views.load_all_products(uow)
        return [attrs.asdict(p) for p in products]


@ns.route("/<int:product_id>")
class ProductEndpoint(Resource):
    @ns.marshal_list_with(product_serializer)
    def get(self, product_id):
        uow = UnitOfWork(db.engine)
        product = views.load_product(uow, product_id)
        return product


@ns.route("/upload-csv")
class ProductUpload(Resource):
    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files:
            return "No file sent", 400
        request_file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if request_file.filename == '':
            return "No selected file", 400

        uploaded_file_path = UPLOAD_FOLDER / request_file.filename
        request_file.save(uploaded_file_path)

        async_result = tasks.load_products_from_csv_task.delay(request_file.filename)
        async_result.get()
        return {"task_id": async_result.id}, 201
