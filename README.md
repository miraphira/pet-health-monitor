# Pet Health Monitor

Simple pet health monitoring dashboard with FastAPI and SQLite.

## Current Features
- Dashboard
- Create, edit, delete, and view health logs
- SQLite database
- Basic summary cards

## Tech Stack
- Python
- FastAPI
- HTML
- CSS
- SQLite
- Jinja2

## Run Project

Activate virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn main:app --reload
```

Open:

```txt
http://localhost:8000
```

## Database

The SQLite database file (`pet.db`) is generated automatically when the application runs for the first time.