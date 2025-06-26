from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.db.connect import connect_db
from app.routers import market

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def startup_event():
    print("🚀 서버 시작됨, DB 연결 시도 중...")
    conn = connect_db()
    if conn:
        print("📡 DB 연결 확인 완료")
        conn.close()
    else:
        print("⚠️ DB 연결 실패, 앱 내부 기능에 영향 있을 수 있음")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.
    startup_event()

    yield

    # When service is stopped.


app = FastAPI(lifespan=lifespan)
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
def read_root():
    return {"message": "Hello, FastAPI"}
