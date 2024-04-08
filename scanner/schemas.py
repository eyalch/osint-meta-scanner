import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from . import models


class ScanCreate(BaseModel):
    domain: str


class Scan(BaseModel):
    id: uuid.UUID
    domain: str
    started_at: Optional[datetime.datetime]
    completed_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True


class Result(BaseModel):
    tool: str
    type: models.Result.Type
    value: str

    class Config:
        from_attributes = True


class ScanWithResults(Scan):
    results: list[Result]
