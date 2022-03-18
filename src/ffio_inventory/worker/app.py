from celery import Celery

from ffio_inventory.repository import db, DATABASE_URL


def load_tasks():
    from ffio_inventory.worker import tasks


celery_app = Celery("tasks")
celery_app.config_from_object("ffio_inventory.worker.config")
load_tasks()
db.init_db(DATABASE_URL)
