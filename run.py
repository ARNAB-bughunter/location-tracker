import os
import uvicorn
from app import app

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    uvicorn.run(app=app, host="0.0.0.0", port=8181)
