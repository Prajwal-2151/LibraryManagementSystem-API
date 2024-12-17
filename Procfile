web: gunicorn LibraryManagementSystem.wsgi --log-file -
worker: celery -A LibraryManagementSystem worker --pool=solo -l info