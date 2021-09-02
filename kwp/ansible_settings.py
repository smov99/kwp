
import sys

# SECURITY WARNING: keep the secret key used in production secret!
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
KWP_AWS_KEY = 'AKIAZXQ6BWHIYPRDXQE7'
KWP_AWS_SECRET = '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'
KWP_S3_RESOURCES = '/dev/resources/'
KWP_S3_PROPOSAL_DOCS = '/dev/proposal-docs/'

# list of resources, non case sensitive
STATIC_RESOURCES = ['show_case_study__c', 'show_quick_start_guide__c', 'show_brochure__c']
#  - show_kiwapower_at_a_glance_video__c    # commented for the following testing

