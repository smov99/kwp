import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kwp.settings')

app = Celery('kwp')
app.conf.enable_utc = False
app.conf.update(timezone='America/New_York')
app.config_from_object('django.conf:settings', namespace='CELERY')
