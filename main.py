from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import connect_db
import random
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def format_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%d %b")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    today_date = datetime.now().strftime("%d %b %Y")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM health_logs 
        ORDER BY created_at DESC 
    """)

    logs = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM health_logs
        ORDER BY created_at DESC LIMIT 5
    """)
    latest_logs = cursor.fetchall()

    cursor.execute("""
        SELECT * 
        FROM health_logs 
        WHERE type = 'berat badan'
        ORDER BY created_at DESC
        LIMIT 1
    """)
    last_weight_log = cursor.fetchone()
    log_weight_dict = dict(last_weight_log)
    weight_date = format_date(log_weight_dict["created_at"])

    cursor.execute("""
        SELECT weight, created_at 
        FROM health_logs
        WHERE type = 'berat badan' 
        ORDER BY created_at
    """)
    weight_logs = cursor.fetchall()

    jml_makan = 0
    jml_muntah = 0
    jml_bab = 0
    jml_obat = 0
    jml_bb = 0
    log_list = []

    for log in logs:
        if log["type"] == "makan":
            jml_makan += 1

        elif log["type"] == "muntah":
            jml_muntah += 1
        
        elif log["type"] == "BAB":
            jml_bab += 1
        
        elif log["type"] == "obat":
            jml_obat += 1
        
        elif log["type"] == "berat badan":
            jml_bb += 1
        
        log_dict = dict(log)
        log_dict["formatted_date"] = format_date(log_dict["created_at"])
        log_list.append(log_dict)
    
    weight_dates = []
    weight_values = []

    for log in weight_logs:
        weight_dates.append(format_date(log["created_at"]))
        weight_values.append(log["weight"])
    conn.close()

    moods = [
    "lapar tapi judging babu",
    "moi mode sinis 😾",
    "lagi flashback kehidupan lampau",
    "menjadi bola hitam",
    "menatap tembok tanpa alasan",
    "bola hitam menunggu makan"
    ]

    if jml_muntah > 5 :
        moi_mood = "Moi sebaiknya ke dokter! 😭"
    elif jml_muntah > 2:
        moi_mood = "Moi berusaha fine 🥺"
    else:
        moi_mood = random.choice(moods)

    return templates.TemplateResponse(
        request= request,
        name= "index.html",
        context={
        "today_date": today_date,
        "logs": log_list,
        "total_logs": len(logs),
        "latest_log": latest_logs,
        "last_weight": last_weight_log,
        "weight_date": weight_date,
        "weight_dates": weight_dates,
        "weight_values": weight_values,
        "mood_moi": moi_mood,
        "jml_makan": jml_makan,
        "jml_muntah": jml_muntah,
        "jml_bab": jml_bab,
        "jml_obat": jml_obat,
        "jml_bb": jml_bb
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
    note: str | None = Form(None),
    weight: float | None = Form(None)
):
    print("===DATA BARU===")
    print("Jenis log: ", log_type)
    print("Catatan: ", note)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO health_logs (type, note, weight)
        VALUES (?, ?, ?)
        """,
        (log_type, note, weight)
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
        note: str | None = Form(None)
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