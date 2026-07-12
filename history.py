import requests
import pandas as pd

BASE_URL = "https://api.india.delta.exchange/v2"


def get_history(symbol="BTCUSD", resolution="5m", limit=300):
    return pd.DataFrame()
