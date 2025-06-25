from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import market
from fastapi.middleware.cors import CORSMiddleware

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()
app.include_router(market.router, prefix="/api")
# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용. 배포시엔 특정 도메인으로 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
