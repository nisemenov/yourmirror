# BUILD
.PHONY: sync-all
sync-all:
	uv sync --all-packages --all-groups


# SERVER
.PHONY: run-backend
run-backend:
	uv run --package yourmirror.backend -- python backend/manage.py runserver

.PHONY: run-link-preview
run-link-preview:
	uv run --package yourmirror.service.link_preview -- uvicorn services.link_preview.app:app --port 8001 --reload

.PHONY: tailwind-install
tailwind-install:
	uv run --package yourmirror.backend -- python backend/manage.py tailwind install

.PHONY: tailwind-start
tailwind-start:
	uv run --package yourmirror.backend -- python backend/manage.py tailwind start


# DOCKER
.PHONY: minio
minio:
	docker exec -it minio bash

.PHONY: psql
psql:
	docker exec -it postgres psql -d yourmirror -U postgres

.PHONY: redis
redis:
	docker exec -it redis redis-cli


# TEST AND LINT
.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv run pytest backend/tests/
