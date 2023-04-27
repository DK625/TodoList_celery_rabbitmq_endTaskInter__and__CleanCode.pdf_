import datetime
import os

from celery import Celery
from celery.schedules import crontab
from ...config import settings

os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")


celery_app = Celery(
    "tasks",
    broker=settings.BROKER_MESSAGE,
    include=["app.src.celery_tasks.tasks"],
)
celery_app.conf.beat_schedule = {
    "check-due-date-every-15-minutes": {
        "task": "check_due_date",
        "schedule": datetime.timedelta(minutes=15),
        # "schedule": datetime.timedelta(seconds=15),
    },
    "announcement_8am_every_day": {
        "task": "morning",
        "schedule": crontab(hour=8, minute=0),
        # "schedule": datetime.timedelta(seconds=15),
    },
    # "check-due-date-every-15-seconds": {
    #     "task": "send_email",
    #     "kwargs": {"message": "ahihi"},
    #     "schedule": datetime.timedelta(seconds=15),
    # },
}
# tự động chạy task check_due_date sau mỗi 15 phút và 8h sáng gửi thông báo
