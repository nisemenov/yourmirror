import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourmirror.settings.dev")

app = Celery("yourmirror")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
