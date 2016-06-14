from .settings import *
import os

password = os.environ['password']
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'winning',
        'USER': 'ubuntu',
        'PASSWORD': password,
        'HOST': '127.0.0.1',
    }
}
