# db/init_db.py
from .database import Base, engine
from .models.index import IndexTypes, IndexData, IndexScore  # 모델들 import


def init_db():
    print("⏳ DB 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✅ 테이블 생성 완료")
