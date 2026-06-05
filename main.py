from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import connect_db
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM health_logs 
        ORDER BY created_at DESC 
    """)

    logs = cursor.fetchall()
    latest_log = logs[0] if logs else None
    conn.close()

    moods = [
    "lapar tapi judging babu",
    "moi mode sinis 😾",
    "lagi flashback kehidupan lampau",
    "menjadi bola hitam",
    "menatap tembok tanpa alasan",
    "bola hitam menunggu makan"
    ]

    moi_mood = random.choice(moods)

    return templates.TemplateResponse(
        request= request,
        name= "index.html",
        context={
        "logs": logs,
        "total_logs": len(logs),
        "latest_log": latest_log,
        "mood_moi": moi_mood
        }
    )

@app.get("/edit/{log_id}")
def edit_page(request: Request, log_id: int):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM health_logs 
        WHERE id = ?
        """, (log_id,)
    )

    log = cursor.fetchone()
    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context=
        {
            "log": log
        }
    )

@app.post("/submit-log")
def submit_log(
    log_type: str = Form(...),
    note: str | None = Form(None)
):
    print("===DATA BARU===")
    print("Jenis log: ", log_type)
    print("Catatan: ", note)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO health_logs (type, note)
        VALUES (?, ?)
        """,
        (log_type, note)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )

@app.post("/delete/{log_id}")
def delete_log(log_id: int):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM health_logs 
        WHERE id = ?
        """,
        (log_id,)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )

@app.post("/update/{log_id}")
def update_log(
        log_id: int,
        log_type: str = Form(...),
        note: str = Form(...)
):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE health_logs 
        SET type = ?, note = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE id = ?
        """, (log_type, note, log_id)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )