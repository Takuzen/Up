from .common import *

DEBUG = False

ALLOWED_HOSTS = [
    'up-env.eba-aesibyxa.us-east-1.elasticbeanstalk.com',
    'www.uplife.link',
    'uplife.link',
    'up-staging.us-east-1.elasticbeanstalk.com',
    'up-https.us-east-1.elasticbeanstalk.com'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

AWS_ACCESS_KEY_ID = 'AKIA4FE4J7NTC37VQI7X'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'up-env-bucket'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 1日はそのキャッシュを使う
}

STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')

DEFAULT_FILE_STORAGE = 'config.settings.storage_backend.MediaStorage'
