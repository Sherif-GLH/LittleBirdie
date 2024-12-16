import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','LittleBirdie.settings')

## instnce of celery application ##
app = Celery('LittleBirdie')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()