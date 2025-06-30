from fastapi import HTTPException
import time
from app.services.vix import fetch_latest_vix
from app.services.fgi import fetch_fear_and_greed
from app.services.calculator import calculate_market_score
from app.utils.cache_store import CacheStore

CACHE_TTL = 60 * 60  # 1시간


async def fetch_index_score():
    now = time.time()
    cache_entry = CacheStore._store.setdefault(
        "index_score", {"data": None, "last_fetched": 0}
    )

    if cache_entry["data"] and (now - cache_entry["last_fetched"]) < CACHE_TTL:
        print("🚀 Returned Fear_and_Greed from cache")
        return cache_entry["data"]

    vix_data = await fetch_latest_vix()
    fgi_data = await fetch_fear_and_greed()
    try:
        vix_value = float(vix_data["value"])
        fgi_value = float(fgi_data["value"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(status_code=500, detail="지표 데이터 파싱 실패")

    result = calculate_market_score(vix_value=vix_value, fgi_value=fgi_value)

    cache_entry["data"] = result
    cache_entry["last_fetched"] = now
    # print(result)
    return result
