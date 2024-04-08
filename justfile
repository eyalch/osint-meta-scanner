#!/usr/bin/env just --justfile

set positional-arguments
set dotenv-load

server:
  uvicorn scanner.main:app --reload

@celery *args:
  celery -A scanner.tasks $@

@alembic *args:
  alembic $@
