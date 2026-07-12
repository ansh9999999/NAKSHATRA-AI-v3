import requests
import pandas as pd

BASE_URL = "https://api.india.delta.exchange/v2"


def get_history(symbol="BTCUSD", resolution="5m"):
    try:
        url = f"{BASE_URL}/history/candles"

        params = {
            "symbol": symbol,
            "resolution": resolution
        }

        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            return pd.DataFrame()

        data = r.json()["result"]

        df = pd.DataFrame(data)

        df = df.rename(columns={
            "time": "timestamp"
        })

        numeric = ["open", "high", "low", "close", "volume"]

        for col in numeric:
            df[col] = df[col].astype(float)

        return df.sort_values("timestamp")

    except Exception as e:
        print(e)
        return pd.DataFrame()
