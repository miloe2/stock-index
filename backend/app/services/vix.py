from datetime import date, timedelta
import httpx
from fastapi import HTTPException
import time
from app.config.settings import FRED_API_KEY

# ---- 캐시 저장소 ----
_cache_store = {
    "vix": {"data": None, "last_fetched": 0},
    "vix_range": {},
}

CACHE_TTL = 60 * 0.5  # 1시간


async def fetch_latest_vix():
    now = time.time()
    cache_entry = _cache_store["vix"]

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

    cache_entry = _cache_store.setdefault(key, {"data": None, "last_fetched": 0})

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
