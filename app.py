import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from logging.handlers import RotatingFileHandler
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="static")


# Optional: Allow CORS (important if calling from frontend/browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_app_logger():
    logger = logging.getLogger(name='app logger')
    if  logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10000000, backupCount=50)
    formatter = logging.Formatter(f"%(asctime)s %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


# Pydantic model to validate the request body
class InputData(BaseModel):
    city: str
    region: str
    country: str
    postal: str
    timezone: str


@app.post("/process")
async def process_data(payload: InputData):
    logger = get_app_logger()
    # Extract values
    city = payload.city
    region = payload.region
    country = payload.country
    postal = payload.postal
    timezone = payload.timezone
    
    
    result = f"Received city={city}, region={region} country={country} postal={postal} timezone={timezone}"
    logger.info(f"RESULT: {result}")
    return {"message": "SUCESS"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
