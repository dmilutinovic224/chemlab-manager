import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projekat.settings')

proapp = Celery('Projekat')
proapp.config_from_object('django.conf:settings', namespace='CELERY')
proapp.autodiscover_tasks()