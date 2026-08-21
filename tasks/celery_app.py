from celery import Celery

from cache.config import REDIS_URL


celery_app = Celery(

    "travel_platform",

    broker=REDIS_URL,

    backend=REDIS_URL
)