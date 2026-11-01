import os

from celery import Celery


celery_app = Celery(
    "tariff_service",
    broker=os.getenv(
        "CELERY_BROKER_URL",
        "redis://localhost:6379/1",
    ),
    backend=os.getenv(
        "CELERY_RESULT_BACKEND",
        "redis://localhost:6379/2",
    ),
    include=[
        "app.tasks",
    ],
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=120,
    task_soft_time_limit=100,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)