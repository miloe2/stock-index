import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def connect_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
        )
        print("✅ DB 연결 성공")
        return conn
    except Exception as e:
        print("❌ DB 연결 실패:", e)
        return None
