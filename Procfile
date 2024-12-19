web: gunicorn LibraryManagementSystem.wsgi --worker-class gevent --log-file -
worker: celery -A LibraryManagementSystem worker --pool=solo -l info