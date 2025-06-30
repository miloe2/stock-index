from fastapi import HTTPException
from datetime import date, timedelta
import time
import httpx
from app.config.settings import FRED_API_KEY
from app.utils.cache_store import CacheStore


CACHE_TTL = 60 * 60  # 1시간


async def fetch_latest_vix():
    now = time.time()
    cache_entry = CacheStore._store.setdefault("vix", {"data": None, "last_fetched": 0})

    if cache_entry["data"] and (now - cache_entry["last_fetched"]) < CACHE_TTL:
        print("🚀 Returned VIX from cache")
        return cache_entry["data"]

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
            latest = observations[-1]
            cache_entry["data"] = latest
            cache_entry["last_fetched"] = now
            print("🔄 Fetched VIX from API and cached")
            return latest  # 가장 최신 데이터
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


async def fetch_range_vix(start_date: str, end_date: str):
    now = time.time()
    key = f"vix_range_{start_date}_{end_date}"
    cache_entry = CacheStore._store.setdefault(key, {"data": None, "last_fetched": 0})

    if cache_entry["data"] and (now - cache_entry["last_fetched"]) < CACHE_TTL:
        print(f"🚀 Returned VIX range from cache for {key}")
        return cache_entry["data"]

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

            cache_entry["data"] = observations
            cache_entry["last_fetched"] = now
            print(f"🔄 Fetched VIX range from API and cached for {key}")
            return observations
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
