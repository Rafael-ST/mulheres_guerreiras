"""
Django settings for mulheresguerreiras project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'S3C43T')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('DEBUG') in ['False', 'false', '0'] else True

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'sso',
    'crispy_forms',
    'import_export',
    'django_admin_listfilter_dropdown',
    'django_select2',
    'bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mulheresguerreiras.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'static', 'templates')],
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

WSGI_APPLICATION = 'mulheresguerreiras.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

USE_SQLITE = True if os.getenv('USE_SQLITE') in ['True', 'true'] else False

if USE_SQLITE and DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'OPTIONS': {
                'timeout': 30,
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }


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

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

THOUSAND_SEPARATOR = '.'

USE_THOUSAND_SEPARATOR = True


if not DEBUG:
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'Strict'
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 15768000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = 'same-origin'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MAX_UPLOAD_SIZE = 429916160

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtps.fortaleza.ce.gov.br'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = '???'
# EMAIL_HOST_PASSWORD = '???'


#Library djangoselect2
SELECT2_JS  = '/static/vendors/js/select2.min.js'
SELECT2_CSS = "/static/vendors/css/select2.min.css"


# Default settings
BOOTSTRAP4 = {
# The complete URL to the Bootstrap CSS file
# Note that a URL can be either a string,
# e.g. "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css",
# or a dict like the default value below.
"css_url": {
"href": "/static/vendors/css/bootstrap.min.css",
},
# The complete URL to the Bootstrap JavaScript file
"javascript_url": {
"url": "/static/vendors/js/bootstrap.min.js",
},
# The complete URL to the Bootstrap CSS file (None means no theme)
"theme_url": None,
# The URL to the jQuery JavaScript file (full)
"jquery_url": {
"url": "/static/vendors/js/jquery.min.js",
},
# The URL to the Popper.js JavaScript file (slim)
"popper_url": {
"url": "/static/vendors/js/popper.min.js",
},
'javascript_in_head': False,
'include_jquery': False,
# Label class to use in horizontal forms
'horizontal_label_class': 'col-md-3',
# Field class to use in horizontal forms
'horizontal_field_class': 'col-md-9',
# Set placeholder attributes to label if no placeholder is provided
'set_placeholder': True,
# Class to indicate required (better to set this in your Django form)
'required_css_class': '',
# Class to indicate error (better to set this in your Django form)
'error_css_class': 'is-invalid',
'success_css_class': 'is-valid',
'formset_renderers':{
'default': 'bootstrap4.renderers.FormsetRenderer',
},
'form_renderers': {
'default': 'bootstrap4.renderers.FormRenderer',
},
'field_renderers': {
'default': 'bootstrap4.renderers.FieldRenderer',
'inline': 'bootstrap4.renderers.InlineFieldRenderer',
},
}