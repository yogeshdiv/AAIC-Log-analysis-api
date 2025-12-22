"""Utility functions for the application."""
from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status


def parse_datetime(value: Optional[str], name: str) -> Optional[datetime]:
    """Parse a datetime string in the format 'YYYY-MM-DD HH:MM:SS'."""
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {name} format. Use YYYY-MM-DD HH:MM:SS",
        ) from exc
