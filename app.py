import os
import logging
import ast
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

def get_app_logger(uuid):
    logger = logging.getLogger(name=uuid)
    if  logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(f'logs/{uuid}.log', maxBytes=10000000, backupCount=50)
    formatter = logging.Formatter(f"%(message)s")
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
    uuid: str


@app.post("/process")
async def process_data(payload: InputData):
    # Extract values
    latitude = payload.latitude
    longitude = payload.longitude
    timestamp = payload.timestamp
    uuid = payload.uuid
    logger = get_app_logger(uuid)
    data = {"latitude": latitude, "longitude": longitude}
    logger.info(data)
    return {"message": "SUCESS"}

@app.get("/view", response_class=HTMLResponse)
def get_last_line_from_latest_file():
    folder_path = "logs"
    # Get all files in the folder with full path
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    if not files:
        return None  # No files found
    
    # Find the latest created file
    latest_file = max(files, key=os.path.getctime)
    
    # Read the last line of that file
    last_line = None
    with open(latest_file, "r", encoding="utf-8") as f:
        for line in f:
            last_line = line.strip()
    
    data = data = ast.literal_eval(last_line)
    lat, long = data['latitude'], data['longitude']
    url = f"https://www.google.com/maps?@{lat},{long}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Dynamic Link Button</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f0f0f0;
                    font-family: Arial, sans-serif;
                }}
                a.button {{
                    padding: 15px 30px;
                    background-color: #28a745;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-size: 18px;
                    transition: background-color 0.3s;
                }}
                a.button:hover {{
                    background-color: #218838;
                }}
            </style>
        </head>
        <body>
            <a class="button" href="{url}" target="_blank">View Location On Google Map</a>
        </body>
    </html>
    """

    return html_content
    


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
