import logging

from celery import Task

from ffio_inventory.core import UPLOAD_FOLDER
from ffio_inventory.repository import db
from ffio_inventory.service import commands
from ffio_inventory.service.uow import UnitOfWork
from ffio_inventory.worker.app import celery_app

log = logging.getLogger(__name__)


@celery_app.task(name='load_products_from_csv', bind=True)
def load_products_from_csv_task(task: Task, file_id: str):
    uow = get_uow()
    csv_file_path = UPLOAD_FOLDER / file_id
    log.info("Start loading file")
    commands.load_products_from_csv(uow, csv_file_path)


def get_uow() -> UnitOfWork:
    return UnitOfWork(db.acquire_engine())
