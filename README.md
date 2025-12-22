# Log Access API

FastAPI service to read tab-separated log files and expose them via REST for filtering and basic analytics.

## Assumptions
- Log files live in `LOG_DIR` (default: `logs/` next to `app/`) and use the format `Timestamp<TAB>Level<TAB>Component<TAB>Message`.
- Only files ending with `.log` are parsed; other files in the directory are ignored.
- Timestamps use `YYYY-MM-DD HH:MM:SS` (naive, assumed UTC). Lines that cannot be parsed or are malformed are skipped.
- `log_id` is deterministic per file/line: `{file_index}-{line_number}` based on alphabetical ordering of `.log` files.
- Pagination is provided via `offset` and `limit` for convenience.

## Getting started
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variable override for log directory:
```bash
# PowerShell
$env:LOG_DIR="C:\path\to\logs"
uvicorn app.main:app --reload
```

Open docs at http://localhost:8000/docs

## API
- `GET /logs`: optional `level`, `component`, `start_time`, `end_time`, `offset`, `limit`, `refresh`.
- `GET /logs/stats`: returns counts per level/component and total.
- `GET /logs/{log_id}`: fetch a single entry.

## Sample data
`logs/sample.log` contains four example entries for quick manual testing.