from datetime import datetime
from typing import Dict
from pydantic import BaseModel


class LogEntrySchema(BaseModel):
    id: str
    timestamp: datetime
    level: str
    component: str
    message: str
    source_file: str
    line_no: int


class LogStatsSchema(BaseModel):
    total: int
    by_level: Dict[str, int]
    by_component: Dict[str, int]
