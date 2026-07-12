import pandas as pd
import numpy as np


def ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()


def sma(df, period):
    return df["close"].rolling(period).mean()


def rsi(df, period=14):
    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def macd(df):
    ema12 = ema(df, 12)
    ema26 = ema(df, 26)

    macd_line = ema12 - ema26
    signal = macd_line.ewm(span=9, adjust=False).mean()

    histogram = macd_line - signal

    return macd_line, signal, histogram


def atr(df, period=14):
    high_low = df["high"] - df["low"]

    high_close = abs(df["high"] - df["close"].shift())

    low_close = abs(df["low"] - df["close"].shift())

    tr = pd.concat(
        [high_low, high_close, low_close],
        axis=1
    ).max(axis=1)

    return tr.rolling(period).mean()
