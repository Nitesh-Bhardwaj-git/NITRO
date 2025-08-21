
## Quick Start

1. **Install dependencies:**

    pip install -r requirements.txt

2. **Apply migrations:**

    python manage.py migrate

3. **Run the development server**

    python manage.py runserver

4. **Upload a CSV file:**

    Send a `POST` request to `/files/upload/` with a file attached in postman.

5. **Check file status and retrieve data:**

    Send a `GET` request to `/files/<file_id>/` to check status or get parsed content.

## API Endpoints

- `POST /files/upload/` — Upload a new CSV file.
- `GET /files/<file_id>/` — Get file status and parsed content (supports query params for filtering).
- `DELETE /files/<file_id>/` — Delete a file.

## Example CSV

Example file: [`csv.txt`](csv.txt)

csv
id,name,email,age,city
1,Alice Johnson,alice@example.com,30,New York
2,Bob Smith,bob@example.com,27,Austin
...