import json
import uuid

import structlog

from scanner.models import Result

from .scanner import Scanner

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class BBOTScanner(Scanner):
    id = "bbot"
    image = "blacklanternsecurity/bbot"

    def scan(self, scan_id: uuid.UUID, domain: str):
        container = self.docker_client.containers.run(
            self.image,
            f"-t {domain} -f subdomain-enum email-enum social-enum cloud-enum -om json --silent",
            detach=True,
            auto_remove=True,
        )

        log = logger.bind(container_id=container.id)

        log.info("Running container")

        for line in container.logs(follow=True, stream=True):
            log.debug("Got container output", line=line)

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            if "type" not in data or "data" not in data:
                continue

            result: tuple[Result.Type, any]
            match data["type"]:
                case "DNS_NAME":
                    result = (Result.Type.DOMAIN, data["data"])
                case "IP_ADDRESS":
                    result = (Result.Type.IP_ADDRESS, data["data"])
                case "ASN":
                    result = (Result.Type.ASN, data["data"]["asn"])
                case "URL":
                    result = (Result.Type.URL, data["data"])
                case "EMAIL_ADDRESS":
                    result = (Result.Type.EMAIL, data["data"])
                case "SOCIAL":
                    result = (
                        Result.Type.SOCIAL,
                        {
                            "platform": data["data"]["platform"],
                            "url": data["data"]["url"],
                        },
                    )
                case "OPEN_TCP_PORT":
                    result = (Result.Type.OPEN_PORT, data["data"])
                case "TECHNOLOGY":
                    result = (
                        Result.Type.TECHNOLOGY,
                        {
                            "host": data["data"]["host"],
                            "technology": data["data"]["technology"],
                        },
                    )
                case _:
                    continue

            self.store_results(scan_id, result)
