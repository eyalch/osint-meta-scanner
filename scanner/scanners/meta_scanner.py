import datetime
import uuid

import docker
import structlog
from sqlalchemy.orm import Session

from scanner import service

from .amass import AmassScanner
from .theharvester import TheHarvesterScanner

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class MetaScanner:
    def __init__(self, db: Session, docker_client: docker.DockerClient):
        self.db = db
        self.scanners = [
            TheHarvesterScanner(db, docker_client),
            AmassScanner(db, docker_client),
        ]

    def scan(self, scan_id: uuid.UUID):
        log = logger.bind(scan_id=scan_id)

        log.info("Getting scan details")

        scan = service.get_scan(self.db, scan_id)

        if scan is None:
            log.error("Scan not found")
            return

        if scan.completed_at is not None:
            log.error("Scan already completed")
            return

        if scan.started_at is not None:
            log.error("Scan already in progress")
            return

        scan.started_at = datetime.datetime.now()
        self.db.commit()

        log = log.bind(domain=scan.domain)

        log.info("Starting scan", started_at=scan.started_at)

        for scanner in self.scanners:
            with structlog.contextvars.bound_contextvars(tool=scanner.id):
                log.info("Scanning with tool")

                scanner.scan(scan.id, scan.domain)

                log.info("Tool scan complete")

        scan.completed_at = datetime.datetime.now()
        self.db.commit()

        log.info("Scan complete", completed_at=scan.completed_at)
