# Production settings

from .base import *

import django_heroku

SECRET_KEY = os.environ.get("SECRET_KEY", "")

DEBUG = False

ALLOWED_HOSTS = ["https://django-blog-1k4z.herokuapp.com/"]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Activate Django-Heroku.
django_heroku.settings(locals())
