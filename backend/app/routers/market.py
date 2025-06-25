from fastapi import APIRouter, HTTPException
from app.services.vix import fetch_latest_vix
from fear_and_greed import get


router = APIRouter()


@router.get("/market/vix")
async def get_vix():
    latest = await fetch_latest_vix()
    if not latest:
        raise HTTPException(status_code=404, detail="VIX data not found")
    return {"date": latest["date"], "value": latest["value"]}


@router.get("/market/fng")
async def get_fear_and_greed():
    result = get()
    return {
        "value": result.value,
        "description": result.description,
        "last_update": result.last_update,
    }
