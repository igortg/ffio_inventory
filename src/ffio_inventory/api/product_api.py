from http import HTTPStatus
from pathlib import Path

import attrs
from flask import request
from flask_restx import Resource, fields, Namespace
from werkzeug.datastructures import FileStorage

from ffio_inventory.core import UPLOAD_PATH
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
    @ns.marshal_with(product_serializer)
    def post(self):
        uow = UnitOfWork(db.engine)
        data = request.json
        new_product = Product(**data)
        new_product = commands.add_product(uow, new_product)
        return new_product, HTTPStatus.CREATED

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
class ProductUploadEndpoint(Resource):
    def post(self):
        if 'file' not in request.files:
            return "No file sent", HTTPStatus.BAD_REQUEST
        request_file: FileStorage = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if request_file.filename == '':
            return "No selected file", HTTPStatus.BAD_REQUEST

        csv_file_path = _save_to_upload_area(request_file)
        async_result = tasks.start_load_products_from_csv(csv_file_path)

        return {"task_id": async_result.id}, HTTPStatus.CREATED


@ns.route("/upload-csv/<task_id>")
class ProductUploadTaskEndpoint(Resource):
    def get(self, task_id):
        state, progress = tasks.get_load_products_from_csv_task_progress(task_id)
        progress["state"] = state
        return progress


def _save_to_upload_area(request_file: FileStorage) -> Path:
    uploaded_file_path = UPLOAD_PATH / request_file.filename
    request_file.save(uploaded_file_path)
    return uploaded_file_path
