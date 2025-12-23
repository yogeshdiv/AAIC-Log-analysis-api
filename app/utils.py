"""Utility functions for the application."""
from datetime import datetime
from typing import Optional


class InvalidDatetimeError(ValueError):
    """Custom exception for invalid datetime format."""
    pass


def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse a datetime string in 'YYYY-MM-DD HH:MM:SS' format."""
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise InvalidDatetimeError("Invalid datetime format YYYY-MM-DD HH:MM:SS") from exc
