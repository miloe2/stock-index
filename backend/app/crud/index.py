from app.db.database import SessionLocal
from app.db.models.index import IndexTypes, IndexData, IndexScore
from app.schemas.index_type import IndexTypeCreate
from app.schemas.index_data import IndexDataCreate
from datetime import date

from typing import Optional
from sqlalchemy.orm import Session
from datetime import date


async def save_index_type(db: Session, data: IndexTypeCreate):
    db_obj = IndexTypes(code=data.code, name=data.name, description=data.description)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


async def save_index_data(db: Session, data: IndexDataCreate):
    # code로 index_type_id 조회
    index_type = db.query(IndexTypes).filter_by(code=data.code.upper()).first()
    if not index_type:
        raise ValueError(f"Invalid index code: {data.code}")

    db_obj = IndexData(index_type_id=index_type.id, date=data.date, value=data.value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# IndexScore 저장
def save_index_score(
    date_: date,
    score: float,
    explanation: Optional[str] = None,
    created_at: Optional[date] = None,
):
    db: Session = SessionLocal()
    try:
        db_score = IndexScore(
            date=date_, score=score, explanation=explanation, created_at=created_at
        )
        db.add(db_score)
        db.commit()
        db.refresh(db_score)
        return db_score
    finally:
        db.close()
