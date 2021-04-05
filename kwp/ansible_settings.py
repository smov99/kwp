# -*- coding: utf-8 -*-

import sys

# debug
DEBUG = True
ENV = 'dev'

# hosts
ALLOWED_HOSTS = [
    '127.0.0.1',
]

# time zone
TIME_ZONE = 'America/New_York'

# dirs
MEDIA_ROOT = '/tmp/kwp'

# static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kwp',
        'USER': 'kwp',
        'PASSWORD': '6zSppdu9ZHy4Q1nB',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# django core
SECRET_KEY = 'at#96-#7p!4bzqreegk@8e&*8whx^ciky5t_o)x04fti31r%8h'

# Salesforce API
SF_CONSUMER_SECRET = 'CD74EE798586E68841BF6CFC60B61B451449904ACDFA3B9E6457D852954FF6B9'
SF_CONSUMER_KEY = '3MVG9M43irr9JAuyX9k4MSEg2sKpL9Eswc9hslkN7vnqYMZxFkIUreh4BiO3HhC..dq9GsWnIqebJDxzQ0CYO'
SF_INITIAL_ACCESS_TOKEN = 'Geosoft#996Cel800D040000008gMG88804000000GndYOHyk2gVh5wcpKjg0OKD7ZhkgtKCImZvHknjlwpDw5RxgucxygvBFwAVS0qlk6taEnGWSQTDx'
SF_USER_NAME= 'smorozov@gmail.com'
SF_API_VERSION = 'v50.0'

# kwp
PRODUCT_VERSION = 'Beta'