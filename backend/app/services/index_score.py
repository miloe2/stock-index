from fastapi import HTTPException
from app.services.vix import fetch_latest_vix
from app.services.fear_and_greed import fetch_fear_and_greed
from app.services.calculator import calculate_market_score


async def fetch_index_score():
    vix_data = await fetch_latest_vix()
    fgi_data = await fetch_fear_and_greed()
    print(vix_data)
    print(fgi_data["last_update"])
    try:
        vix_value = float(vix_data["value"])
        fgi_value = float(fgi_data["value"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(status_code=500, detail="지표 데이터 파싱 실패")

    result = calculate_market_score(vix_value=vix_value, fgi_value=fgi_value)
    # print(result)
    return result
