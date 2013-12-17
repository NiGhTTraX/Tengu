from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tengu.db',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 0,  # never expire, unless evicted
    }
}

# Add django-jenkins
INSTALLED_APPS += (
    'django_jenkins',
)
JENKINS_TASKS = (
    'selenose.tasks.selenium_driver',
)

# Django Compressor settings.
COMPRESS_CSSTIDY_BINARY = '/usr/bin/csstidy'
COMPRESS_YUI_BINARY = 'java -jar /home/nightcrawler/Downloads/yuicompressor-2.4.8.jar'

