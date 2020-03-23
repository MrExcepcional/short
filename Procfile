release: python manage.py migrate
web: gunicorn gettingstarted.wsgi --log-file -
worker: celery worker --app=gettingstarted --loglevel=info
