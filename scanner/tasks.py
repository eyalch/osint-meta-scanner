import os
import uuid

from celery import Celery

from .database import Session
from .logger import configure_logging

configure_logging()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery("scanner", broker=redis_url)
celery.conf.broker_connection_retry_on_startup = False


@celery.task
def scan(scan_id: uuid.UUID):
    import docker

    from .scanners import MetaScanner

    docker_client = docker.from_env()

    with Session() as session:
        MetaScanner(session, docker_client).scan(scan_id)
