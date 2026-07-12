import pandas as pd


def ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()


def sma(df, period):
    return df["close"].rolling(period).mean()


def rsi(df, period=14):
    delta = df["close"].diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss

    return 100 - (100 / (1 + rs))
