from analysis.indicators import (
    ema,
    rsi,
    macd,
    atr,
    adx,
    volume_spike,
    trend_strength,
)


def generate_signal(df):

    price = float(df["close"].iloc[-1])

    score = 0
    reasons = []

    # =====================
    # EMA
    # =====================

    ema9 = ema(df, 9).iloc[-1]
    ema21 = ema(df, 21).iloc[-1]

    bullish = ema9 > ema21

    if bullish:
        score += 20
        reasons.append("EMA Bullish")
    else:
        score -= 20
        reasons.append("EMA Bearish")

    # =====================
    # RSI
    # =====================

    rsi14 = rsi(df).iloc[-1]

    if bullish and rsi14 > 55:
        score += 15
        reasons.append("RSI Strong")

    elif (not bullish) and rsi14 < 45:
        score -= 15
        reasons.append("RSI Weak")

    # =====================
    # MACD
    # =====================

    macd_line, signal_line, hist = macd(df)

    if macd_line.iloc[-1] > signal_line.iloc[-1]:
        score += 15
        reasons.append("MACD Bullish")

    else:
        score -= 15
        reasons.append("MACD Bearish")

    # =====================
    # ADX
    # =====================

    adx14 = adx(df).iloc[-1]

    if adx14 > 25:
        score += 10
        reasons.append("Strong Trend")

    # =====================
    # ATR
    # =====================

    atr14 = atr(df).iloc[-1]

    if atr14 > atr(df).tail(20).mean():
        score += 10
        reasons.append("ATR Expansion")

    # =====================
    # Volume Spike
    # =====================

    if volume_spike(df).iloc[-1]:
        score += 10
        reasons.append("Volume Spike")

    # =====================
    # BREAKOUT
    # =====================

    high20 = df["high"].tail(20).max()

    low20 = df["low"].tail(20).min()

    if bullish and price >= high20:
        score += 10
        reasons.append("Resistance Breakout")

    if (not bullish) and price <= low20:
        score -= 10
        reasons.append("Support Breakdown")

    # =====================
    # SIGNAL
    # =====================

    if score >= 90:

        signal = "BIG BUY"

    elif score <= -90:

        signal = "BIG SELL"

    else:

        signal = "WAIT"

    confidence = min(abs(score), 100)

    return {

        "signal": signal,

        "confidence": confidence,

        "score": score,

        "price": round(price, 2),

        "trend": trend_strength(df),

        "ema9": round(float(ema9), 2),

        "ema21": round(float(ema21), 2),

        "rsi": round(float(rsi14), 2),

        "adx": round(float(adx14), 2),

        "atr": round(float(atr14), 2),

        "reasons": reasons

    }
