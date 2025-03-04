import re
import uuid

import structlog

from scanner.models import Result

from .scanner import Scanner

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class AmassScanner(Scanner):
    id = "amass"
    image = "caffix/amass"

    def scan(self, scan_id: uuid.UUID, domain: str):
        container = self.docker_client.containers.run(
            self.image,
            f"enum -d {domain}",
            detach=True,
            auto_remove=True,
        )

        log = logger.bind(container_id=container.id)

        log.info("Running container")

        for line in container.logs(follow=True, stream=True):
            log.debug("Got container output", line=line)

            if match := re.search(
                r"^(.*) \((\w+)\) --> \w+ --> (.*) \((\w+)\)$",
                line.decode().strip(),
            ):
                from_val, from_type, to_val, to_type = match.groups()

                self.handle_result(scan_id, from_type, from_val)
                self.handle_result(scan_id, to_type, to_val)

    def handle_result(self, scan_id: uuid.UUID, typ: str, result: str):
        mapped_type: Result.Type
        match typ:
            case "FQDN":
                mapped_type = Result.Type.DOMAIN
            case "IPAddress":
                mapped_type = Result.Type.IP_ADDRESS
            case "ASN":
                mapped_type = Result.Type.ASN
            case _:
                return

        self.store_results(scan_id, (mapped_type, result))
