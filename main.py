from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request= request,
        name= "index.html"
    )

@app.post("/submit-log")
def submit_log(
    log_type: str = Form(...),
    note: str = Form(...)
):
    print("===DATA BARU===")
    print("Jenis log: ", log_type)
    print("Catatan: ", note)

    return {
        "message": "Log berhasil diterima!",
        "log_type": log_type,
        "note": note
    }
