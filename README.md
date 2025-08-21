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

### Use with Thunder Client (VS Code)

Base URL: `http://localhost:8000`

1) Upload a file (POST /files)
- New Request → Method: POST → URL: `http://localhost:8000/files`
- Body → Form → add key `file` (Type: File) → choose your file
- Send → you should get a response like:
```json
{"file_id":"<uuid>", "status":"uploading", "progress":0}
```

2) Save `file_id` for reuse (Thunder Client variable)
- In the same request, open the Tests tab and paste:
```javascript
const json = JSON.parse(response.body);
tc.setVar('file_id', json.file_id);
```
- From now on, you can reference `{{file_id}}` in request URLs.

3) Poll progress (GET /files/{file_id}/progress)
- New Request → GET → `http://localhost:8000/files/{{file_id}}/progress`
- Repeat until you get:
```json
{"file_id":"<uuid>", "status":"ready", "progress":100}
```

4) Get parsed content (GET /files/{file_id})
- GET → `http://localhost:8000/files/{{file_id}}`
- If still processing, status will be 202 with a message.

5) List files (GET /files)
- GET → `http://localhost:8000/files`
- Response:
```json
{"files":[{"id":"<uuid>","filename":"sample.csv","status":"ready","created_at":"2025-01-01T12:00:00Z"}]}
```

6) Delete a file (DELETE /files/{file_id})
- DELETE → `http://localhost:8000/files/{{file_id}}`
- Response: `{ "deleted": true }`

Tips
- No auth or special headers required.
- Upload uses multipart form-data with key `file`.
- `file_id` is a UUID; Thunder Client variables make reuse easy.

