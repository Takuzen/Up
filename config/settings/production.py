from .common import *

DEBUG = False

ALLOWED_HOSTS = [
    'up-tokyo.us-east-1.elasticbeanstalk.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['RDS_Up'],
        'USER': os.environ['RDS_db_user'],
        'PASSWORD': os.environ['RDS_password'],
        'HOST': os.environ['RDS_172.20.0.3'],
        'PORT': os.environ['RDS_3306'],
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')