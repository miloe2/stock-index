from datetime import date, timedelta
import httpx

import pandas as pd
from fastapi import HTTPException
from app.config.settings import FRED_API_KEY


async def fetch_sp500_deviation():
    today = date.today()
    start_date = (today - timedelta(days=300)).isoformat()  # 여유 있게 300일치 확보
    end_date = today.isoformat()

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "SP500",
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
            # print(data)
            observations = data.get("observations", [])
            if len(observations) < 200:
                return None  # 이동평균 계산 불가

            # pandas로 변환
            df = pd.DataFrame(observations)
            df["date"] = pd.to_datetime(df["date"])
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna().set_index("date").sort_index()

            # 200일 이동평균 및 이격도 계산
            df["MA200"] = df["value"].rolling(window=200).mean()
            latest = df.iloc[-1]
            deviation = (latest["value"] - latest["MA200"]) / latest["MA200"] * 100

            return {
                "date": latest.name.date().isoformat(),
                "current_value": latest["value"],
                "ma200": latest["MA200"],
                "deviation_percent": round(deviation, 2),
            }

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
