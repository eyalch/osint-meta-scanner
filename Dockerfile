# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

USER appuser

WORKDIR /app


FROM base AS base-deps

ENV PATH="/home/appuser/.local/bin:$PATH"

RUN pip install --user poetry==1.8.2 \
    && python -m venv venv

ENV VIRTUAL_ENV="/app/venv"

COPY pyproject.toml poetry.lock ./


FROM base-deps AS server-deps

RUN poetry install --sync --with=server


FROM base-deps AS worker-deps

RUN poetry install --sync --with=worker


FROM base AS server

COPY --from=server-deps /app/venv ./venv
COPY . .

EXPOSE 8000

CMD ["uvicorn", "scanner.main:app", "--host=0.0.0.0", "--port=8000"]

HEALTHCHECK CMD curl --fail http://localhost:8000/scans || exit 1


FROM base AS worker

COPY --from=worker-deps /app/venv ./venv
COPY . .

CMD ["celery", "-A", "scanner.tasks", "worker", "--loglevel=info"]

HEALTHCHECK CMD ["celery", "-A", "scanner.tasks", "inspect", "ping"]
