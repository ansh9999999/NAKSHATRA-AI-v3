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

def vwap(df):
    tp = (df["high"] + df["low"] + df["close"]) / 3
    return (tp * df["volume"]).cumsum() / df["volume"].cumsum()


def volume_spike(df, period=20, multiplier=2):
    avg = df["volume"].rolling(period).mean()
    return df["volume"] > (avg * multiplier)


def adx(df, period=14):
    plus_dm = df["high"].diff()
    minus_dm = -df["low"].diff()

    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0)
    minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0)

    tr = pd.concat([
        df["high"] - df["low"],
        abs(df["high"] - df["close"].shift()),
        abs(df["low"] - df["close"].shift())
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()

    plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

    dx = ((plus_di - minus_di).abs() / (plus_di + minus_di)) * 100

    return dx.rolling(period).mean()


def trend_strength(df):
    e9 = ema(df, 9)
    e21 = ema(df, 21)

    if e9.iloc[-1] > e21.iloc[-1]:
        return "BULLISH"

    elif e9.iloc[-1] < e21.iloc[-1]:
        return "BEARISH"

    return "SIDEWAYS"
