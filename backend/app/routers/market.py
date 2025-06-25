from fastapi import APIRouter, HTTPException
from app.services.vix import fetch_latest_vix
from app.services.sp500 import fetch_sp500_deviation
from fear_and_greed import get


router = APIRouter()


@router.get("/market/vix")
async def get_vix():
    latest = await fetch_latest_vix()
    if not latest:
        raise HTTPException(status_code=404, detail="VIX data not found")
    # return {"date": latest["date"], "value": latest["value"]}
    return latest


@router.get("/market/sp500")
async def get_sp500_deviation():
    deviation = await fetch_sp500_deviation()
    if not deviation:
        raise HTTPException(status_code=404, detail="VIX data not found")
    # return {"date": deviation["date"], "current_value": deviation["current_value"]}
    return deviation


@router.get("/market/fgi")
async def get_fear_and_greed():
    result = get()
    return {
        "value": result.value,
        "description": result.description,
        "last_update": result.last_update,
    }
