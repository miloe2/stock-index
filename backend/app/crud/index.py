from app.db.database import SessionLocal
from app.db.models.index import IndexTypes, IndexData, IndexScore
from app.schemas.index_type import IndexTypeCreate
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


# IndexData 저장
def save_index_data(
    index_type_id: str, date_: date, value: float, created_at: Optional[date] = None
):
    db: Session = SessionLocal()
    try:
        db_data = IndexData(
            index_type_id=index_type_id, date=date_, value=value, created_at=created_at
        )
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data
    finally:
        db.close()


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
