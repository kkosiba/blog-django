release: python manage.py migrate --settings=website.settings.production
web: gunicorn website.wsgi --log-file -
