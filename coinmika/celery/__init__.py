from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coinmika.settings')

app = Celery('coinmika')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'get_coins_data_from_coingecko_30s': {'task': 'coins.tasks.get_coins_data_from_coingecko', 'schedule': 60.0},
}
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.CELERY_TIMEZONE = 'UTC'
app.autodiscover_tasks()

# web: daphne coinmika.asgi:application --port $PORT --bind 0.0.0.0 -v2
# worker: python manage.py runworker --settings=coinmika.settings -v2
# celery -A coinmika worker -l INFO --concurrency 1 -P solo
# celery -A coinmika beat -l INFO
