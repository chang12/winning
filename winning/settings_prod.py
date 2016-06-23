from .settings import *

password = os.environ['PASSWORD']
# SECRET_KEY = os.environ['SECRET_KEY']
DOMAIN_NAME = "http://winning.fakenerd.kr"

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'winning_db',
        'USER': 'winning_admin',
        'PASSWORD': password,
        'HOST': 'localhost',
        'PORT': '',
    }
}
