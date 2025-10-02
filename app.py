import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from logging.handlers import RotatingFileHandler
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in degrees")
    accuracy: Optional[float] = Field(None, ge=0.0, description="Estimated accuracy in meters")
    altitude: Optional[float] = Field(None, description="Altitude in meters (nullable)")
    speed: Optional[float] = Field(None, ge=0.0, description="Speed in m/s (nullable)")
    heading: Optional[float] = Field(None, ge=0.0, le=360.0, description="Heading in degrees (nullable)")
    timestamp: datetime = Field(..., description="ISO 8601 timestamp")


@app.post("/process")
async def process_data(payload: InputData):
    logger = get_app_logger()
    # Extract values
    latitude = payload.latitude
    longitude = payload.longitude
    timestamp = payload.timestamp
    result = f"Received latitude={latitude}, longitude={longitude} timestamp={timestamp}"
    logger.info(f"RESULT: {result}")
    return {"message": "SUCESS"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
