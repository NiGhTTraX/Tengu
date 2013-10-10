import os
from .base import *


SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split()

STATIC_ROOT = os.environ.get('STATIC_ROOT', '/var/www/static/')
STATIC_URL = os.environ.get('STATIC_URL', 'http://localhost/static/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ['DATABASE_LOCATION'],
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.environ['MEMCACHE_LOCATION'],
    }
}

# Django Compressor settings.
COMPRESS_CSSTIDY_BINARY = os.environ.get('CSSTIDY', '/usr/bin/csstidy')
COMPRESS_YUI_BINARY = os.environ.get('YUI', 'java -jar %s' % os.path.join(BASE_DIR, 'yuicompressor.jar'))

