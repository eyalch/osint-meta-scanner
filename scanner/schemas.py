import datetime
import uuid
from typing import Any

from pydantic import BaseModel

from . import models


class ScanCreate(BaseModel):
    domain: str


class Scan(BaseModel):
    id: uuid.UUID
    domain: str
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None

    class Config:
        from_attributes = True


class Result(BaseModel):
    tool: str
    type: models.Result.Type
    value: str | dict[str, Any]

    class Config:
        from_attributes = True


class ScanWithResults(Scan):
    results: list[Result]
