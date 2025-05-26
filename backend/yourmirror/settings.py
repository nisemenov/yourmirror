import environ
import os

from pathlib import Path

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

environ.Env.read_env(os.path.join(PROJECT_ROOT, ".env"))

DEBUG = env("DEBUG")
PROD_MODE = env.bool("PROD_MODE", default=False)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = [
    "*",
    "127.0.0.1",
    "localhost",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "tailwind",
    "theme",
    "minio_storage",
    "profiles.apps.ProfilesConfig",
    "wishitems.apps.WishitemsConfig",
    "services.apps.ServicesConfig",
]

if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]

TAILWIND_APP_NAME = "theme"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

ROOT_URLCONF = "yourmirror.urls"

TEMPLATES_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "context_processors.footer.year",
            ],
        },
    },
]

WSGI_APPLICATION = "yourmirror.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


# Password validation
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

# MinIO базовые параметры
MINIO_STORAGE_ENDPOINT = f"{env('MINIO_HOST')}:{env('MINIO_PORT')}"
MINIO_STORAGE_ACCESS_KEY = env("MINIO_ROOT_USER")
MINIO_STORAGE_SECRET_KEY = env("MINIO_ROOT_PASSWORD")
MINIO_STORAGE_USE_HTTPS = env.bool("MINIO_SECURE", default=False)

# Бакеты
MINIO_STORAGE_MEDIA_BUCKET_NAME = "media"
MINIO_STORAGE_STATIC_BUCKET_NAME = "static"
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_AUTO_CREATE_MEDIA_POLICY = "READ_WRITE"

STORAGES = {
    "default": {
        "BACKEND": "minio_storage.storage.MinioMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# URLs
if DEBUG:
    FULL_DOMAIN = "http://127.0.0.1:8000"
else:
    FULL_DOMAIN = ""

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = f"http://{env('MINIO_HOST')}:{env('MINIO_PORT')}/media/"
MEDIA_ROOT = BASE_DIR / "media"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOGIN_URL = "login"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1

if PROD_MODE:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_PORT = 465
    EMAIL_USE_SSL = True
    EMAIL_HOST = env("EMAIL_HOST", default="")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="")

if DEBUG:
    REDIS_HOST = "localhost"
else:
    REDIS_HOST = "redis"

CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":6379/0"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
