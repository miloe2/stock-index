from datetime import date, timedelta
import httpx
from fastapi import HTTPException
from app.config.settings import FRED_API_KEY


async def fetch_latest_vix():
    today = date.today()
    start_date = (today - timedelta(days=7)).isoformat()
    end_date = today.isoformat()

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "VIXCLS",
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url, params=params)
            res.raise_for_status()
            data = res.json()
            observations = data.get("observations", [])
            if not observations:
                return None
            return observations[-1]  # 가장 최신 데이터
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


async def fetch_range_vix(start_date: str, end_date: str):

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "VIXCLS",
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url, params=params)
            res.raise_for_status()
            data = res.json()
            observations = data.get("observations", [])
            if not observations:
                return None
            return observations
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
