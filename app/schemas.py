from datetime import datetime
from typing import Dict
from pydantic import BaseModel


class LogEntrySchema(BaseModel):
    """Schema representing a single log entry."""
    id: str
    timestamp: datetime
    level: str
    component: str
    message: str
    source_file: str
    line_no: int


class LogStatsSchema(BaseModel):
    """Schema representing log statistics."""
    total: int
    by_level: Dict[str, int]
    by_component: Dict[str, int]
