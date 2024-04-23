"""
Django settings for exchange project.

Generated by "django-admin startproject" using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

import environ
from corsheaders.defaults import default_headers
from rest_framework import authentication

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Build paths inside the project like this: BASE_DIR / "subdir".


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True
USE_X_FORWARDED_HOST = True
CORS_ALLOW_HEADERS = [
    *default_headers,
    "x-role",
    "X-Role"
]
CORS_EXPOSE_HEADERS = [
    *default_headers,
    "x-role",
    "X-Role"
]

APPS = [
    "users",
    "authority",
    "authentication",
    "api",
    "creditcard",
    "wallet",
    "bitpin",
    "order",
    "zarinpal",
    "permission",
    "commission",
    "ticket",
    "config",
    "jibit",
    "referral"
]
LIBS = [
    "rest_framework",
    "drf_yasg",
    "knox",
    "corsheaders",
    "django_crontab",
    "solo"
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *LIBS,
    *APPS

]
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "bitasia.ir"]
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = ["http://localhost", "https://api.bitasia.ir", "https://dashborad.bitasia.ir",
                        "https://bitasia.ir"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF = "exchange.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "exchange.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASS"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "fa"

TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ("fa", "Persian")
]

LOCALE_PATHS = ("locale/",)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend",
                           "authentication.backend.OtpAuthBackend"]
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
    "EXCEPTION_HANDLER": "exchange.utils.custom_exception_handler",
    'DEFAULT_THROTTLE_RATES': {
        'forget-password': '60/hour',
        'forget-password-apply': '2/day'
    }
}
REST_KNOX = {
    "AUTH_HEADER_PREFIX": "Bearer",
    "TOKEN_TTL": timedelta(hours=72),
}
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {
            "type": "basic"
        },
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}
OTP_EXPIRE_MINUTES = 30

CRONJOBS = [
    ("* * * * *", "bitpin.crons.get_bitpin_currencies_cron", ">> /srv/bitasia-django/log.log"),
    ("* * * * *", "authentication.crons.check_otp_expiration", ">> /srv/bitasia-django/otp/log.log"),
    ("* */12 * * *", "jibit.crons.update_token", ">> /srv/bitasia-django/jibit/log.log"),
]
