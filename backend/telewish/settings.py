import environ
import os
from pathlib import Path


env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

environ.Env.read_env(os.path.join(PROJECT_ROOT, ".env"))

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = [
    "*",
    "127.0.0.1",
    "localhost",
]

# for login
LOGIN_REMEMBER_ME = env("LOGIN_REMEMBER_ME", default=0)


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
    "django_browser_reload",
    "theme",
    "minio_storage",
    "profiles.apps.ProfilesConfig",
    "wishitems.apps.WishitemsConfig",
]

TAILWIND_APP_NAME = "theme"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "telewish.urls"

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

WSGI_APPLICATION = "telewish.wsgi.application"


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
