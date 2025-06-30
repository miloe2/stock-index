from fear_and_greed import get
from app.utils.cache_store import CacheStore
import time


CACHE_TTL = 60 * 60  # 1시간


async def fetch_fear_and_greed():
    now = time.time()
    cache_entry = CacheStore._store.setdefault("fgi", {"data": None, "last_fetched": 0})

    if cache_entry["data"] and (now - cache_entry["last_fetched"]) < CACHE_TTL:
        print("🚀 Returned Fear_and_Greed from cache")
        return cache_entry["data"]
    rsp = get()
    result = {
        "value": rsp.value,
        "description": rsp.description,
        "last_update": rsp.last_update,
    }

    cache_entry["data"] = result
    cache_entry["last_fetched"] = now
    return result
