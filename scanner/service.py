import csv
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Result, Scan


def check_in_progress_scan(db: Session, domain: str) -> bool:
    stmt = select(Scan).filter_by(domain=domain, completed_at=None)
    scan = db.execute(stmt).scalar_one_or_none()
    return scan is not None


def create_scan(db: Session, domain: str):
    scan = Scan(domain=domain)
    db.add(scan)
    db.commit()
    return scan


def get_scans(db: Session):
    stmt = select(Scan)
    return db.execute(stmt).scalars().all()


def get_scan(db: Session, scan_id: uuid.UUID):
    stmt = select(Scan).filter_by(id=scan_id)
    return db.execute(stmt).scalar_one_or_none()


class DummyWriter:
    @staticmethod
    def write(line):
        return line


def generate_results_csv(results: list[Result]):
    writer = csv.DictWriter(DummyWriter(), fieldnames=["tool", "type", "value"])

    yield writer.writeheader()

    for result in results:
        yield writer.writerow(
            {
                "tool": result.tool,
                "type": result.type.value,
                "value": result.value,
            }
        )
