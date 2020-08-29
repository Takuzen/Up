from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0"]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Up',  # ←.env_sampleで指定したMYSQL_DATABASE
        'USER': 'db_user',  # ←.env_sampleで指定したMYSQL_USER
        'PASSWORD': 'password',  # ←.env_sampleで指定したMYSQL_PASSWORD
        'HOST': '172.20.0.3',  # ←docker-compose.ymlに指定したmysqlのIPAddress
        'PORT': '3306',
    }
}


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

INTERNAL_IPS += ['0.0.0.0']
