#!/bin/bash

set -e  # Завершить скрипт с ошибкой в случае неудачи

if [ "$MAIN_BACKEND_CONTAINER" = "1" ]; then  # Только в базовом контейнере
    python manage.py collectstatic --noinput
    python manage.py migrate --noinput
fi

exec "$@"  # CMD из Dockerfile
