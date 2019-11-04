from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

WSGI_APPLICATION = 'djangoAPI.wsgi.production.application'

ALLOWED_HOSTS = ['*', 'youflix.ssafy.io', '13.125.172.87']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': DEBUG,
        'BUNDLE_DIR_NAME': '/bundles/',  # must end with slash
        'STATS_FILE': os.path.join(FRONTEND_DIR, 'webpack-stats.json'),
    }
}