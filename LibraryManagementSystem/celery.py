from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryManagementSystem.settings')

app = Celery('LibraryManagementSystem')

app.conf.update(
          enable_utc=False,
          timezone='Asia/Kolkata',
          broker_connection_retry_on_startup=True,
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
          print(f'Request: {self.request!r}')
