## File Parser CRUD API with Progress Tracking

### Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run server:
   ```bash
   python manage.py runserver 8000
   ```

### APIs
- POST `/files` (multipart `file`): start upload + async parse (CSV). Returns `{file_id, status, progress}`.
- GET `/files/{file_id}/progress`: returns `{file_id, status, progress}`.
- GET `/files/{file_id}`: if ready, returns `{file_id, status, content}`; else 202 with message.
- GET `/files`: list uploaded files `{files: [{id, filename, status, created_at}]}`.
- DELETE `/files/{file_id}`: delete file and parsed content.

Notes:
- Files stored under `MEDIA_ROOT` (`media/`).
- Parsing is simulated asynchronously via a background thread and supports CSV via `csv.DictReader`.

