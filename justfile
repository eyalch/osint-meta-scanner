#!/usr/bin/env just --justfile

set positional-arguments
set dotenv-load

server:
  uvicorn scanner.main:app --reload --host ${HOST:-127.0.0.1} --port ${PORT:-8000}

@celery *args:
  celery -A scanner.tasks $@

@alembic *args:
  alembic $@
