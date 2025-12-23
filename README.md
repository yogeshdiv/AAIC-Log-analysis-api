## Log Access API

A small FastAPI service that reads log files from disk and exposes them over a REST API for querying and basic analysis.

The service is read-only and is intended to make it easy to inspect and filter log data without importing it into a database.

## Assumptions & Design Notes

Log files are read from a directory defined by LOG_DIR (defaults to a logs/ folder next to the app/ directory).

Each log entry is expected to be a single line in the format:
Timestamp<TAB>Level<TAB>Component<TAB>Message

Only files with a .log extension are processed. Any other files in the directory are ignored.

Timestamps must follow the format YYYY-MM-DD HH:MM:SS and are treated as naive/UTC.

Malformed lines or lines with invalid timestamps are skipped rather than causing the service to fail.

Each log entry is assigned a deterministic log_id using the pattern {file_index}-{line_number}, where files are ordered alphabetically.

Logs are cached in memory and reloaded only when files change or when explicitly requested.

Pagination is supported using offset and limit to avoid returning very large responses.

## Running the Service

Install dependencies

`pip install -r requirements.txt`

Start the API

`uvicorn app.main:app --reload`

## Once running, interactive API documentation is available at:

`http://localhost:8000/docs`

## API Endpoints

`GET /logs`

Returns log entries with optional filters:

1. level

2. component

3. start_time

4. end_time

5. offset

6. limit

7. refresh (forces reload from disk)

`GET /logs/stats`

Returns basic statistics:

1. total log count

2. count per log level

3. count per component

`GET /logs/{log_id}`

Returns a single log entry by its log_id.

## Sample Data

A small example log file is provided at:

`logs/sample.log`
