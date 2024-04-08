import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Scan


def get_scan(db: Session, scan_id: uuid.UUID):
    stmt = select(Scan).filter_by(id=scan_id)
    return db.execute(stmt).scalar_one_or_none()
