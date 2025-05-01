# SERVER
.PHONY: run-server
run-server:
	uv run --package your_mirror.backend -- python manage.py runserver

.PHONY: static
static:
	uv run --package your_mirror.backend -- python manage.py collectstatic


# MIGRATIONS
.PHONY: makemigrations
makemigrations:
	uv run --package your_mirror.backend -- python manage.py makemigrations

.PHONY: migrate
migrate:
	uv run --package your_mirror.backend -- python manage.py migrate


# TEST AND LINT
.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv run pytest tests/
