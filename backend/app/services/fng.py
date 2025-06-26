from fear_and_greed import get


async def fetch_fear_and_greed():
    result = get()
    return {
        "value": result.value,
        "description": result.description,
        "last_update": result.last_update,
    }
