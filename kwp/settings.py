"""
Django settings for kwp project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'at#96-#7p!4bzqreegk@8e&*8whx^ciky5t_o)x04fti31r%8h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '*',
]

# Application definition

DEFAULT_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rangefilter',
]

LOCAL_APPS = [
    'proposal.apps.ProposalConfig',
    'faq.apps.CeleryConfig',
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kwp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

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

REST_FRAMEWORK = {
}

# Salesforce API
SF_CONSUMER_SECRET = 'CD74EE798586E68841BF6CFC60B61B451449904ACDFA3B9E6457D852954FF6B9'
SF_CONSUMER_KEY = '3MVG9M43irr9JAuyX9k4MSEg2sKpL9Eswc9hslkN7vnqYMZxFkIUreh4BiO3HhC..dq9GsWnIqebJDxzQ0CYO'
SF_INITIAL_ACCESS_TOKEN = 'Geosoft999Cel800D040000008gMG88804000000GndYOHyk2gVh5wcpKjg0OKD7ZhkgtKCImZvHknjlwpDw5RxgucxygvBFwAVS0qlk6taEnGWSQTDx'
SF_USER_NAME = 'smorozov@gmail.com'
SF_API_VERSION = 'v51.0'
SF_PASSWORD = 'ge0s0ft99'
SF_LOGIN_URL = 'https://test.salesforce.com/services/oauth2/token'
SF_USER_ID = '0056g0000036ZdTAAU'

TRUSTED_EMAIL = 'backdoor@email.com'

SESSION_COOKIE_AGE = 600
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Authentication parameters

AUTH_USER_MODEL = 'users.User'


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'src/log.log'),
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ('es', gettext('ES')),
    ('en', gettext('EN-US')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'tmp/static/')

MEDIA_URL = '/tmp/kwp/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'tmp/kwp/')

# kwp
PRODUCT_VERSION = 'Beta'
