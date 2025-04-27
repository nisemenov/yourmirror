# SERVER
run-server:
	uv run --package your_mirror.backend -- python manage.py runserver


# MIGRATIONS
makemigrations:
	uv run --package your_mirror.backend -- python manage.py makemigrations

migrate:
	uv run --package your_mirror.backend -- python manage.py migrate


# TEST AND LINT
lint:
	uv run pre-commit run --all-files

test:
	uv run pytest tests/
