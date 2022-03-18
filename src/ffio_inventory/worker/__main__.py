import sys

from ffio_inventory.worker.app import celery_app


def init_worker():
    args = sys.argv[:]
    args.pop(0)
    if sys.platform == "win32":
        # Should be used only for development
        args.append("--pool=gevent")

    celery_app.worker_main(args)


if __name__ == "__main__":
    init_worker()
