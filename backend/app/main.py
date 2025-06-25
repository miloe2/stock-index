from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import market

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()
app.include_router(market.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
