import os
import uvicorn
from app import app
from app import get_app_logger


if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    get_app_logger()
    uvicorn.run(app=app, host="0.0.0.0", port=8181)
