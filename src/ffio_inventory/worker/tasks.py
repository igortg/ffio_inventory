import logging
from pathlib import Path

from celery import Task, states
from celery.result import AsyncResult

from ffio_inventory.core import UPLOAD_PATH
from ffio_inventory.repository import db
from ffio_inventory.service import commands
from ffio_inventory.service.uow import UnitOfWork
from ffio_inventory.worker.app import celery_app

log = logging.getLogger(__name__)


def start_load_products_from_csv(csv_filepath: Path) -> AsyncResult:
    """
    Start to process the given CSV file with a list of products in an
    asynchronous fashion and returns the Task ID.
    """
    uploaded_file = csv_filepath.relative_to(UPLOAD_PATH)
    async_result = _load_products_from_csv_task.delay(uploaded_file)
    return async_result


def get_load_products_from_csv_task_progress(task_id: str) -> tuple[str, dict]:
    """
    Query the state and progress on the given Celery `task_id`.

    :return: Task state and a dict with the "current" and "total" keywords.
    """
    from celery.states import STARTED

    async_result = celery_app.AsyncResult(task_id)
    progress = async_result.result if async_result.state == STARTED else {}
    return async_result.state, progress


@celery_app.task(name='load_products_from_csv', bind=True)
def _load_products_from_csv_task(task: Task, file_id: str):
    log.info("Start loading file")
    uow = get_uow()
    csv_file_path = UPLOAD_PATH / file_id

    def task_progress_callback(msg, current, total):
        log.info(f"{current//1000}K of {total//1000}K")
        _progress_state = {"current": current, "total": total}
        task.update_state(state=states.STARTED, meta=_progress_state)

    commands.load_products_from_csv(uow, csv_file_path, progress_callback=task_progress_callback)


def get_uow() -> UnitOfWork:
    return UnitOfWork(db.acquire_engine())
