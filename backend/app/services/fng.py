from fear_and_greed import get

# ---- 캐시 저장소 ----
_cache_store = {
    "vix": {"data": None, "last_fetched": 0},
    "vix_range": {},
}

CACHE_TTL = 60 * 0.5  # 1시간


async def fetch_fear_and_greed():
    result = get()
    return {
        "value": result.value,
        "description": result.description,
        "last_update": result.last_update,
    }
