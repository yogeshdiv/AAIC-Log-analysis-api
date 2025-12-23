"""Repository module for managing log entries from log files in a directory."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


@dataclass
class LogEntry:
    """Data class representing a single log entry."""
    id: str
    timestamp: datetime
    level: str
    component: str
    message: str
    source_file: str
    line_no: int

    def to_dict(self) -> dict[str, object]:
        """Convert the LogEntry to a dictionary."""
        return asdict(self)


class LogRepository:
    """Repository for managing log entries from log files in a directory."""
    def __init__(self, log_dir: Path):
        """Initialize the LogRepository with the given log directory."""
        self.log_dir = log_dir
        self._cache: Optional[List[LogEntry]] = None
        self._signature: Optional[Tuple[Tuple[str, float, int], ...]] = None

    def _directory_signature(self) -> Tuple[Tuple[str, float, int], ...]:
        """Generate a signature of the log directory based on file names, modification times, and sizes."""
        parts: List[Tuple[str, float, int]] = []
        if not self.log_dir.exists():
            return tuple()
        for path in sorted(self.log_dir.glob("*.log")):
            if path.is_file():
                stat = path.stat()
                parts.append((path.name, stat.st_mtime, stat.st_size))
        return tuple(parts)

    def _load_entries(self) -> List[LogEntry]:
        """Load log entries from log files in the directory."""
        entries: List[LogEntry] = []
        file_paths = [p for p in sorted(self.log_dir.glob("*.log")) if p.is_file()]
        for file_idx, path in enumerate(file_paths):
            with path.open("r", encoding="utf-8") as handle:
                for line_no, raw_line in enumerate(handle, start=1):
                    line = raw_line.strip()
                    if not line:
                        continue
                    parts = line.split("\t", 3)
                    if len(parts) != 4:
                        continue
                    timestamp_str, level, component, message = parts
                    try:
                        ts = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        continue
                    log_id = f"{file_idx}-{line_no}"
                    entries.append(
                        LogEntry(
                            id=log_id,
                            timestamp=ts,
                            level=level.strip(),
                            component=component.strip(),
                            message=message.strip(),
                            source_file=path.name,
                            line_no=line_no,
                        )
                    )
        return entries

    def _refresh_cache_if_needed(self, force: bool = False) -> None:
        """Refresh the cache of log entries if the directory has changed or if forced."""
        current_sig = self._directory_signature()
        if force or self._cache is None or self._signature != current_sig:
            self._cache = self._load_entries()
            self._signature = current_sig

    def get_entries(self, refresh: bool = False) -> List[LogEntry]:
        """Get all log entries, refreshing cache if needed."""
        self._refresh_cache_if_needed(force=refresh)
        return list(self._cache or [])

    def get_entry(self, log_id: str, refresh: bool = False) -> Optional[LogEntry]:
        """Get a specific log entry by its ID."""
        self._refresh_cache_if_needed(force=refresh)
        if not self._cache:
            return None
        for entry in self._cache:
            if entry.id == log_id:
                return entry
        return None

    def filter_entries(
        self,
        entries: Iterable[LogEntry],
        level: Optional[str] = None,
        component: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[LogEntry]:
        """Filter log entries based on criteria."""
        filtered: List[LogEntry] = []
        for entry in entries:
            if level and entry.level.lower() != level.lower():
                continue
            if component and entry.component.lower() != component.lower():
                continue
            if start_time and entry.timestamp < start_time:
                continue
            if end_time and entry.timestamp > end_time:
                continue
            filtered.append(entry)
        return filtered

    def stats(self, entries: Iterable[LogEntry]) -> Tuple[int, dict[str, int], dict[str, int]]:
        """Compute statistics: total count, count by level, count by component."""
        total = 0
        by_level: dict[str, int] = {}
        by_component: dict[str, int] = {}
        for entry in entries:
            total += 1
            by_level[entry.level] = by_level.get(entry.level, 0) + 1
            by_component[entry.component] = by_component.get(entry.component, 0) + 1
        return total, by_level, by_component
