
import sys

# SECURITY WARNING: keep the secret key used in production secret!
from datetime import timedelta

SECRET_KEY = 'at#96-#7p!4bzqreegk@8e&*8whx^ciky5t_o)x04fti31r%8h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ['127.0.0.1']

ALLOWED_HOSTS = [
    '*',
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kwp',
        'USER': 'kwp',
        'PASSWORD': '6zSppdu9ZHy4Q1nB',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Cache settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_DB_ID = '4'
REDIS_DB_CELERY_ID = '5'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_ID}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'kiwapower'
    }
}

# Celery settings

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_CELERY_ID}'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TIMEZONE = 'America/New_York'

# JWT settings

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

SF_CONSUMER_SECRET = '6687B3551B44B14613450674FD6D2F5948B206FB0F6872E5E0E07617D9482299'
SF_CONSUMER_KEY = '3MVG9AJuBE3rTYDgjVgTfUitelQPY_J9j15W4eFxHPuOoTmShEk3gN82WbE2Bu68qMyP5vj_bILwpnS2nclWh'
SF_USER_NAME = 'django@kiwapower.com.july16'
SF_API_VERSION = 'v51.0'
SF_PASSWORD = 'Ge0s0ft#99'
SF_LOGIN_URL = 'https://test.salesforce.com/services/oauth2/token'
SF_USER_ID = '0055x00000BFIezAAH'
TRUSTED_EMAIL = 'backdoor@email.com'

# IP geolocation
IPDATA_TOKEN = '5d721175bef6ff7756ec1ef843876cbf5e3559fb2f1c051f46ff9dec'

# stage 2
ENV = 'dev'

# S3
KWP_S3 = 'kwp-001'
KWP_S3_RESOURCES = 'dev/resources/'
KWP_S3_PROPOSAL_DOCS = 'dev/proposal-docs/'
