from celery import Celery
import os
import datetime
from celery.schedules import crontab


os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")


celery_app = Celery(
    "tasks",
    broker="amqp://roegjsyb:GLm6HM5YrT0XlJY34oJxPcyKFyftBv9-@armadillo.rmq.cloudamqp.com/roegjsyb",
    # include=["app.src.celery.tasks"],
    include=["app.src.celery_tasks.tasks"],
)
celery_app.conf.beat_schedule = {
    'check-due-date-every-15-minutes': {
        'task': 'app.src.celery_tasks.tasks.check_due_date',
        'schedule': datetime.timedelta(minutes=15),
    },
    'announcement_8am_every_day': {
        'task': 'app.src.celery_tasks.tasks.morning',
        'schedule': crontab(hour=8, minute=0),
    }
}
# tự động chạy task check_due_date sau mỗi 15 phút và 8h sáng gửi thông báo
