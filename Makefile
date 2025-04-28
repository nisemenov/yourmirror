# BUILD
.PHONY: sync-all
sync-all:
	uv sync --all-packages --all-groups


# SERVER
.PHONY: run-backend
run-backend:
	uv run --package your_mirror.backend -- python backend/manage.py runserver

.PHONY: run-link-preview
run-link-preview:
	uv run --package your_mirror.service.link_preview -- uvicorn services.link_preview.app:app --port 8001 --reload

.PHONY: tailwind-install
tailwind-install:
	uv run --package your_mirror.backend -- python backend/manage.py tailwind install

.PHONY: tailwind-start
tailwind-start:
	uv run --package your_mirror.backend -- python backend/manage.py tailwind start


# DOCKER
.PHONY: minio
minio:
	docker exec -it minio bash

.PHONY: psql
psql:
	docker exec -it postgres psql -d telewish -U postgres


# TEST AND LINT
.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv run pytest backend/tests/
