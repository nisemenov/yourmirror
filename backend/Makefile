# SERVER
.PHONY: run-server
run-server:
	uv run --package yourmirror.backend -- python manage.py runserver --settings=yourmirror.settings.dev

.PHONY: static
static:
	uv run --package yourmirror.backend -- python manage.py collectstatic --settings=yourmirror.settings.dev

.PHONY: celery-start
celery-start:
	uv run --package yourmirror.backend -- celery -A yourmirror worker --loglevel=INFO


# MIGRATIONS
.PHONY: makemigrations
makemigrations:
	uv run --package yourmirror.backend -- python manage.py makemigrations --settings=yourmirror.settings.dev

.PHONY: migrate
migrate:
	uv run --package yourmirror.backend -- python manage.py migrate --settings=yourmirror.settings.dev


# TEST AND LINT
.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: mypy
mypy:
	uv run pre-commit run mypy --all-files

.PHONY: test
test:
	uv run pytest tests/
