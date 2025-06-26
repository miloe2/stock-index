from app.services.vix import fetch_latest_vix
from app.services.fear_and_greed import fetch_fear_and_greed
from app.services.calculator import normalize_fgi, normalize_vix, calculate_market_score


async def fetch_index_score():
    vix_data = await fetch_latest_vix()
    fgi_data = await fetch_fear_and_greed()
    vix_value = normalize_vix(vix_value=float(vix_data["value"]))
    fgi_value = normalize_fgi(fgi_value=float(fgi_data["value"]))
    result = calculate_market_score(vix_value=vix_value, fgi_value=fgi_value)
    # print(result)
    return result
