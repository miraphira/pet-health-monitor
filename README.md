# Pet Health Monitor

Simple pet health monitoring dashboard with FastAPI and SQLite.

## Current Features
- User authentication
- Secure password hashing with bcrypt
- Dashboard
- Create, edit, delete, and view health logs
- SQLite database
- Basic summary cards
- Weight statistics for tracking
- Latest activity
- Random status

## Tech Stack
- Python
- FastAPI
- HTML
- CSS
- SQLite
- Jinja2
- Chart.js

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