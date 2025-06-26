from fastapi import APIRouter, HTTPException, Query
from app.services.vix import fetch_latest_vix, fetch_range_vix
from app.services.sp500 import fetch_sp500_deviation
from app.services.fear_and_greed import fetch_fear_and_greed
from app.services.index_score import fetch_index_score


router = APIRouter()


@router.get("/market/vix")
async def get_vix():
    latest = await fetch_latest_vix()
    if not latest:
        raise HTTPException(status_code=404, detail="VIX data not found")
    # return {"date": latest["date"], "value": latest["value"]}
    return latest


@router.get("/market/vix/range")
async def get_range_vix(
    start_date: str = Query(..., description="조회 시작일 (YYYY-MM-DD)"),
    end_date: str = Query(..., description="조회 종료일 (YYYY-MM-DD)"),
):
    result = await fetch_range_vix(start_date, end_date)
    if not result:
        raise HTTPException(status_code=404, detail="VIX data not found")
    # return {"date": latest["date"], "value": latest["value"]}
    return result


@router.get("/market/sp500")
async def get_sp500_deviation():
    deviation = await fetch_sp500_deviation()
    if not deviation:
        raise HTTPException(status_code=404, detail="VIX data not found")
    # return {"date": deviation["date"], "current_value": deviation["current_value"]}
    return deviation


@router.get("/market/fgi")
async def get_fear_and_greed():
    result = fetch_fear_and_greed()
    return {result}


@router.get("/market/score")
async def get_index_score():
    try:
        result = await fetch_index_score()
        return {"score": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"지표 계산 실패: {str(e)}")
