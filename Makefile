# BUILD
sync-all:
	uv sync --all-packages --all-groups


# SERVER
run-backend:
	uv run --package your_mirror.backend -- python backend/manage.py runserver

run-link-preview:
	uv run --package your_mirror.service.link_preview -- uvicorn services.link_preview.app:app --port 8001 --reload

tailwind-install:
	uv run --package your_mirror.backend -- python backend/manage.py tailwind install

tailwind-start:
	uv run --package your_mirror.backend -- python backend/manage.py tailwind start


# DOCKER
minio:
	docker exec -it minio bash

psql:
	docker exec -it postgres psql -d telewish -U postgres


# TEST AND LINT
lint:
	uv run pre-commit run --all-files

test:
	uv run pytest backend/tests/
