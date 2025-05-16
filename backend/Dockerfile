FROM python:3.13 AS uv-base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=/usr/local/bin/python3.13 \
    UV_PROJECT_ENVIRONMENT=/appenv \
    UV_LOCKED=1

FROM uv-base AS shell-venv
COPY backend/pyproject.toml /src/backend/
COPY services/link_preview/pyproject.toml /src/services/link_preview/
COPY pyproject.toml uv.lock /src/
RUN <<EOT
cd /src
uv sync --no-install-workspace --package yourmirror.backend --no-install-project
EOT

FROM python:3.13
ENV PYTHONPATH="/appenv: $PYTHONPATH"
ENV PATH="/appenv/bin: $PATH"
COPY --from=shell-venv /appenv /appenv/
WORKDIR /app

COPY backend/entrypoint.sh /app
ENTRYPOINT ["/app/entrypoint.sh"]
