import logging

from flask import Flask
from flask_restx import Api

from ffio_inventory.api.product_api import ns as product_ns
from ffio_inventory.core import UPLOAD_PATH
from ffio_inventory.repository import db

log = logging.getLogger(__name__)


def create_app(db_url: str) -> Flask:
    app = Flask(__name__)

    upload_path = UPLOAD_PATH
    upload_path.mkdir(exist_ok=True)

    api = Api(title='Products Inventory API')
    api.add_namespace(product_ns)

    api.init_app(app)

    log.info(f"Setting database to: {db_url}")
    db.init_db(db_url)

    @app.teardown_appcontext
    def close_connection(exc):
        db.acquire_engine().dispose()

    @app.route("/is_alive")
    def is_alive() -> str:
        return "OK"

    return app
