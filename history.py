import time
import requests
import pandas as pd

BASE_URL = "https://api.india.delta.exchange/v2"


def get_history(symbol="BTCUSD", resolution="5m", limit=200):

    seconds = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "30m": 1800,
        "1h": 3600,
        "4h": 14400,
        "1d": 86400,
    }

    candle_seconds = seconds.get(resolution, 300)

    now = int(time.time())

    end = now - (now % candle_seconds)
    start = end - (limit * candle_seconds)

    url = f"{BASE_URL}/history/candles"

    params = {
        "symbol": symbol,
        "resolution": resolution,
        "start": start,
        "end": end,
    }

    try:

        r = requests.get(url, params=params, timeout=15)

        print("=" * 60)
        print("STATUS :", r.status_code)
        print("URL :", r.url)

        data = r.json()

        print("RESPONSE :")
        print(data)
        print("=" * 60)

        if r.status_code != 200:
            return pd.DataFrame()

        if "result" not in data:
            print("No result key found")
            return pd.DataFrame()

        df = pd.DataFrame(data["result"])

        if df.empty:
            print("Empty DataFrame")
            return df

        print("Columns :", df.columns.tolist())
        print(df.tail())

        numeric = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        for col in numeric:
            if col in df.columns:
                df[col] = df[col].astype(float)

        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"], unit="s")

        df = df.sort_values("time")
        df.reset_index(drop=True, inplace=True)

        return df

    except Exception as e:

        print("History Error :", e)

        return pd.DataFrame()
