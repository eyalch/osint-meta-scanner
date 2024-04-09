import re
import uuid

import structlog

from .scanner import ResultType, Scanner

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class AmassScanner(Scanner):
    id = "amass"
    image = "amass"

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
            s = line.decode().strip()

            log.debug("Got container output", line=s)

            if match := re.search(r"^(.*) \((\w+)\) --> \w+ --> (.*) \((\w+)\)$", s):
                from_val, from_type, to_val, to_type = match.groups()

                self.handle_result(scan_id, from_type, from_val)
                self.handle_result(scan_id, to_type, to_val)

    def handle_result(self, scan_id: uuid.UUID, typ: str, result: str):
        mapped_type: ResultType
        match typ:
            case "FQDN":
                mapped_type = ResultType.DOMAIN
            case "IPAddress":
                mapped_type = ResultType.IP_ADDRESS
            case "ASN":
                mapped_type = ResultType.ASN
            case _:
                return

        self.store_results(scan_id, (mapped_type, result))
