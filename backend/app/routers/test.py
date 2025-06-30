from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.services.vix import fetch_latest_vix, fetch_range_vix
from app.services.sp500 import fetch_sp500_deviation
from app.services.fgi import fetch_fear_and_greed
from app.services.index_score import fetch_index_score
from app.crud.index import save_index_type, save_index_data
from app.schemas.index_type import IndexTypeCreate
from app.schemas.index_data import IndexDataCreate
from app.services.vix import get_and_save_vix

from app.db.database import get_db


router = APIRouter()


# 실제 데이터 DB에 넣기
@router.post("/test/index-data")
async def insert_data(db: Session = Depends(get_db)):
    rst = await get_and_save_vix(db, "2025-04-18", "2025-06-30")
    return rst
