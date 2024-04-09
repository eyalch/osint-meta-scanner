import datetime
import uuid

from pydantic import BaseModel, Json

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
    value: Json

    class Config:
        from_attributes = True


class ScanWithResults(Scan):
    results: list[Result]
