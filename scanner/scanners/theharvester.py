import json
import uuid

import structlog

from .scanner import ResultType, Scanner

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class TheHarvesterScanner(Scanner):
    id = "theharvester"
    image = "theharvester"

    def scan(self, scan_id: uuid.UUID, domain: str):
        container = self.docker_client.containers.run(
            self.image,
            f"sh -c '/root/.local/bin/theHarvester -b anubis,baidu,bing,bingapi,certspotter,crtsh,dnsdumpster,duckduckgo,hackertarget,otx,rapiddns,sitedossier,subdomaincenter,subdomainfinderc99,threatminer,urlscan,yahoo -d {domain} -f out > /dev/null && cat out.json'",
            entrypoint="",
            detach=True,
            auto_remove=True,
        )

        log = logger.bind(container_id=container.id)

        log.info("Running container")

        output = container.logs(follow=True)

        log.debug("Got container output", output=output)

        data = json.loads(output)

        results = []

        if "asns" in data:
            results += [
                (ResultType.ASN, asn.removeprefix("AS")) for asn in data["asns"]
            ]
        if "emails" in data:
            results += [(ResultType.EMAIL, email) for email in data["emails"]]
        if "hosts" in data:
            results += [(ResultType.DOMAIN, host) for host in data["hosts"]]
        if "ips" in data:
            results += [(ResultType.IP_ADDRESS, ip) for ip in data["ips"]]
        if "interesting_urls" in data:
            results += [(ResultType.URL, url) for url in data["interesting_urls"]]

        self.store_results(scan_id, results)
