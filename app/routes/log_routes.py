"""Routes for log access and statistics."""
import os
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.repository import LogRepository
from app.schemas import LogEntrySchema, LogStatsSchema
from app.utils import parse_datetime
router = APIRouter()

LOG_DIR = Path(os.getenv("LOG_DIR", Path(__file__).resolve().parent.parent / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

repository = LogRepository(LOG_DIR)

def get_repository() -> LogRepository:
    """Dependency to get the LogRepository instance."""
    return repository

@router.get("/logs", response_model=List[LogEntrySchema])
def list_logs(
    level: Optional[str] = Query(None, description="Filter by log level"),
    component: Optional[str] = Query(None, description="Filter by component"),
    start_time: Optional[str] = Query(
        None, description="Filter logs after this timestamp (YYYY-MM-DD HH:MM:SS)"
    ),
    end_time: Optional[str] = Query(
        None, description="Filter logs before this timestamp (YYYY-MM-DD HH:MM:SS)"
    ),
    refresh: bool = Query(False, description="Force reload from disk"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(
        1000, ge=1, le=10_000, description="Maximum number of records to return"
    ),
    repo: LogRepository = Depends(get_repository),
):
    """List log entries with optional filtering and pagination."""
    start_dt = parse_datetime(start_time, "start_time")
    end_dt = parse_datetime(end_time, "end_time")

    entries = repo.get_entries(refresh=refresh)
    print(entries)
    print(start_dt, end_dt)
    filtered = repo.filter_entries(
        entries,
        level=level,
        component=component,
        start_time=start_dt,
        end_time=end_dt,
    )
    paged = filtered[offset : offset + limit] if limit else filtered[offset:]
    return [LogEntrySchema(**entry.to_dict()) for entry in paged]


@router.get("/logs/stats", response_model=LogStatsSchema)
def log_stats(
    refresh: bool = Query(False, description="Force reload from disk"),
    repo: LogRepository = Depends(get_repository),
):
    entries = repo.get_entries(refresh=refresh)
    total, by_level, by_component = repo.stats(entries)
    return LogStatsSchema(total=total, by_level=by_level, by_component=by_component)


@router.get("/logs/{log_id}", response_model=LogEntrySchema)
def get_log(
    log_id: str,
    refresh: bool = Query(False, description="Force reload from disk"),
    repo: LogRepository = Depends(get_repository),
):
    entry = repo.get_entry(log_id, refresh=refresh)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log with id {log_id} not found",
        )
    return LogEntrySchema(**entry.to_dict())
