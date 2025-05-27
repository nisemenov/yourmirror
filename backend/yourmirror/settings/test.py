from .base import (
    AUTH_PASSWORD_VALIDATORS as AUTH_PASSWORD_VALIDATORS,
    BASE_DIR,
    DEFAULT_AUTO_FIELD as DEFAULT_AUTO_FIELD,
    INSTALLED_APPS as INSTALLED_APPS,
    LANGUAGE_CODE as LANGUAGE_CODE,
    LOGIN_URL as LOGIN_URL,
    MIDDLEWARE as MIDDLEWARE,
    PROJECT_ROOT as PROJECT_ROOT,
    ROOT_URLCONF as ROOT_URLCONF,
    SITE_ID as SITE_ID,
    STATICFILES_DIRS as STATICFILES_DIRS,
    STATIC_URL as STATIC_URL,
    TEMPLATES as TEMPLATES,
    TEMPLATES_DIR as TEMPLATES_DIR,
    TIME_ZONE as TIME_ZONE,
    USE_I18N as USE_I18N,
    USE_TZ as USE_TZ,
    WSGI_APPLICATION as WSGI_APPLICATION,
)

DEBUG = False

SECRET_KEY = "bd1@i20-z#05cj4fdj$xp%758k9*-dtn@fores4tn&xx920@ui"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

FULL_DOMAIN = "http://127.0.0.1:8000"

MEDIA_ROOT = BASE_DIR / "test_media"
STATIC_ROOT = BASE_DIR / "test_static"

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
