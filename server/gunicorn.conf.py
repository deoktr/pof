import multiprocessing
import os

# otherwise we have a single worker, which is less than ideal
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))

worker_class = "gunicorn.workers.ggevent.GeventWorker"

worker_connections = int(os.environ.get("GUNICORN_WORKER_CONNECTIONS", "1000"))
