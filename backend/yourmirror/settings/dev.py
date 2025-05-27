from .base import (
    AUTH_PASSWORD_VALIDATORS as AUTH_PASSWORD_VALIDATORS,
    BASE_DIR,
    DEBUG,
    DEFAULT_AUTO_FIELD as DEFAULT_AUTO_FIELD,
    INSTALLED_APPS,
    LANGUAGE_CODE as LANGUAGE_CODE,
    LOGIN_URL as LOGIN_URL,
    MIDDLEWARE,
    PROJECT_ROOT as PROJECT_ROOT,
    ROOT_URLCONF as ROOT_URLCONF,
    SITE_ID as SITE_ID,
    STATICFILES_DIRS as STATICFILES_DIRS,
    STATIC_ROOT as STATIC_ROOT,
    STATIC_URL as STATIC_URL,
    TAILWIND_APP_NAME as TAILWIND_APP_NAME,
    TEMPLATES as TEMPLATES,
    TEMPLATES_DIR as TEMPLATES_DIR,
    TIME_ZONE as TIME_ZONE,
    USE_I18N as USE_I18N,
    USE_TZ as USE_TZ,
    WSGI_APPLICATION as WSGI_APPLICATION,
    env,
)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "*"]

if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]

if DEBUG:
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

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

FULL_DOMAIN = "http://127.0.0.1:8000"

MEDIA_URL = f"http://{env('MINIO_HOST')}:{env('MINIO_PORT')}/media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="")

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
