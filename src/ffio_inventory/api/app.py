import logging
from flask import Flask, g

from ffio_inventory.api.product import ns as product_ns
from flask_restx import Api

from ffio_inventory.models import db

log = logging.getLogger(__name__)


def create_app(db_url: str) -> Flask:
    app = Flask(__name__)
    app.add_url_rule("/is_alive", view_func=is_alive)

    api = Api(title='Products Inventory API')
    api.add_namespace(product_ns)

    api.init_app(app)

    log.info(f"Setting database to: {db_url}")
    db.init_db(db_url)

    @app.teardown_appcontext
    def close_connection(exc):
        db.acquire_engine().dispose()

    return app


def is_alive() -> str:
    return "OK"
