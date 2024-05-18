from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import io

from sql.database import SessionLocal
from sql.model import PDF

from sql import schemas
from run import Main, GR

templates = Jinja2Templates(directory="static/html")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get('/', response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get('/room', response_class=HTMLResponse)
async def chat_room(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})


@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    try:
        file_data = await file.read()
        db = SessionLocal()
        pdf_file = PDF(file_data=file_data)
        db.add(pdf_file)
        db.commit()
        db.refresh(pdf_file)
        db.close()
        return {"message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post('/question')
async def question(message: schemas.Message):
    db = SessionLocal()
    pdf_file = db.query(PDF).filter(PDF.id > 0).first()
    db.close()
    if not pdf_file:
        raise HTTPException(status_code=404, detail="File not found")
    pdf_content = io.BytesIO(pdf_file.file_data)
    start = datetime.now()
    print(f'Start time: {start}')
    vs = Main(pdf_content).prepare_data()
    response = GR(vector_store=vs, question=message.message).generate_response()
    message.message = str(response)
    end = datetime.now()
    print(f"Total time elapsed: {end - start}")
    return {"message": f"{message.message}"}
