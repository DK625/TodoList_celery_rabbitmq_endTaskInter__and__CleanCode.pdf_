import os

from celery import Celery

os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")


celery_app = Celery(
    "tasks",
    broker="amqp://roegjsyb:GLm6HM5YrT0XlJY34oJxPcyKFyftBv9-@armadillo.rmq.cloudamqp.com/roegjsyb",
    # include=["app.src.celery.tasks"],
    include=["app.src.celery_tasks.tasks"],
)
