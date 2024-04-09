import datetime
import enum
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Scan(Base):
    __tablename__ = "scan"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    domain: Mapped[str]
    started_at: Mapped[datetime.datetime | None]
    completed_at: Mapped[datetime.datetime | None]

    results: Mapped[list["Result"]] = relationship(back_populates="scan")

    def __repr__(self):
        return f"Scan(id={str(self.id)!r}, domain={self.domain!r})"


class Result(Base):
    class Type(enum.Enum):
        FQDN = "fqdn"
        IP_ADDRESS = "ip_address"
        EMAIL = "email"
        URL = "url"
        ASN = "asn"

    __tablename__ = "result"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scan.id"))
    tool: Mapped[str]
    type: Mapped[Type]
    value: Mapped[str]

    __table_args__ = (
        UniqueConstraint("scan_id", "tool", "type", "value", name="unique_result"),
    )

    scan: Mapped[Scan] = relationship(back_populates="results")

    def __repr__(self):
        return f"Result(scan_id={self.scan_id!r}, tool={self.tool!r}, type={self.type!r}, value={self.value!r})"
