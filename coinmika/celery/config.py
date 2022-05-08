import os

from django.conf.global_settings import TIME_ZONE

uri = os.environ.get("CELERY_BROKER_URL")

# Celery Settings
CELERY_BROKER_URL = uri
CELERY_RESULT_BACKEND = "django-db"
BROKER_POOL_LIMIT = None
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE