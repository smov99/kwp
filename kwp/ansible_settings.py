
import sys

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'at#96-#7p!4bzqreegk@8e&*8whx^ciky5t_o)x04fti31r%8h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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

# Salesforce API
SF_CONSUMER_SECRET = 'CD74EE798586E68841BF6CFC60B61B451449904ACDFA3B9E6457D852954FF6B9'
SF_CONSUMER_KEY = '3MVG9M43irr9JAuyX9k4MSEg2sKpL9Eswc9hslkN7vnqYMZxFkIUreh4BiO3HhC..dq9GsWnIqebJDxzQ0CYO'
SF_INITIAL_ACCESS_TOKEN = 'Geosoft999Cel800D040000008gMG88804000000GndYOHyk2gVh5wcpKjg0OKD7ZhkgtKCImZvHknjlwpDw5RxgucxygvBFwAVS0qlk6taEnGWSQTDx'
SF_USER_NAME = 'smorozov@gmail.com'
SF_API_VERSION = 'v51.0'
SF_PASSWORD = '_geosoft99'
SF_LOGIN_URL = 'https://test.salesforce.com/services/oauth2/token'
SF_USER_ID = '0056g0000036ZdTAAU'

TRUSTED_EMAIL = 'backdoor@email.com'

# IP geolocation
IPDATA_TOKEN = '5d721175bef6ff7756ec1ef843876cbf5e3559fb2f1c051f46ff9dec'

# stage 2
env = dev

# S3
kwp_s3: kwp-001
kwp_aws_key: AKIAZXQ6BWHIYPRDXQE7
kwp_aws_secret: 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
kwp_s3_resources: /dev/resources/
kwp_s3_proposal-docs: /dev/proposal-docs/

# list of resources, non case sensitive
static_resources:
  - show_case_study__c
  - show_quick_start_guide__c
  - show_brochure__c
#  - show_kiwapower_at_a_glance_video__c    # commented for the following testing

