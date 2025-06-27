from .config import SessionLocal
from .models import IndexTypes, IndexData, IndexScore
from datetime import date

from typing import Optional
from sqlalchemy.orm import Session
from datetime import date


# IndexTypes 저장
def save_index_type(
    code: str, name: Optional[str] = None, description: Optional[str] = None
):
    db: Session = SessionLocal()
    try:
        db_type = IndexTypes(code=code, name=name, description=description)
        db.add(db_type)
        db.commit()
        db.refresh(db_type)
        return db_type
    finally:
        db.close()


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


# def save_index_score(index_type: str, value: float, d: date):
#     db = SessionLocal()
#     try:
#         db_metric = IndexMetric(index_type=index_type, value=value, date=d)
#         db.add(db_metric)
#         db.commit()
#         db.refresh(db_metric)
#         return db_metric
#     finally:
#         db.close()
