import logging
import shutil
from pathlib import Path

from flask import Flask
from flask_restx import Api

from ffio_inventory.api import api_config
from ffio_inventory.api.product import ns as product_ns
from ffio_inventory.core import UPLOAD_FOLDER
from ffio_inventory.repository import db

log = logging.getLogger(__name__)


def create_app(db_url: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(api_config)

    upload_path = UPLOAD_FOLDER
    if upload_path.is_dir():
        shutil.rmtree(upload_path)
    upload_path.mkdir()

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
