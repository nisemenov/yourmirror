# DEV COMMANDS
minio:
	docker exec -it minio bash

psql:
	docker exec -it postgres psql -d telewish -U postgres

tailwind:
	python manage.py tailwind start


# MIGRATIONS
makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate


# LINT
lint:
	uv run pre-commit run --all-files
