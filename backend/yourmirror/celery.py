import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourmirror.settings")

app = Celery("yourmirror")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
