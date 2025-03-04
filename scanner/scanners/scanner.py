import uuid
from abc import ABC, abstractmethod

import docker
import structlog
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from scanner.models import Result

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class Scanner(ABC):
    def __init__(self, db: Session, docker_client: docker.DockerClient):
        self.db = db
        self.docker_client = docker_client

    @property
    @abstractmethod
    def id(self):
        pass

    @abstractmethod
    def scan(self, scan_id: uuid.UUID, domain: str):
        pass

    def store_results(
        self,
        scan_id: uuid.UUID,
        results: tuple[Result.Type, any] | list[tuple[Result.Type, any]],
    ):
        logger.info("Storing results")

        if not isinstance(results, list):
            results = [results]

        values = [
            {
                "scan_id": scan_id,
                "tool": self.id,
                "type": typ.name,
                "value": value,
            }
            for typ, value in results
        ]
        self.db.execute(insert(Result).values(values).on_conflict_do_nothing())
        self.db.commit()
