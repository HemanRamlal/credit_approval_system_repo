import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "credit_approval_system.settings")
app = Celery("cas_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()