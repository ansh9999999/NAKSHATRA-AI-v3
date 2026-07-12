from analysis.indicators import (
    ema,
    rsi,
    macd,
    atr,
    vwap,
    adx,
    volume_spike,
    trend_strength,
)


def generate_signal(df):

    ema9 = ema(df, 9)
    ema21 = ema(df, 21)

    rsi14 = rsi(df)

    macd_line, signal_line, hist = macd(df)

    atr14 = atr(df)

    vwap_line = vwap(df)

    adx14 = adx(df)

    spike = volume_spike(df)

    score = 0
    reasons = []

    if ema9.iloc[-1] > ema21.iloc[-1]:
        score += 20
        reasons.append("EMA Bullish")
    else:
        score -= 20
        reasons.append("EMA Bearish")

    if rsi14.iloc[-1] > 60:
        score += 20
        reasons.append("RSI Strong")
    elif rsi14.iloc[-1] < 40:
        score -= 20
        reasons.append("RSI Weak")

    if macd_line.iloc[-1] > signal_line.iloc[-1]:
        score += 20
        reasons.append("MACD Bullish")
    else:
        score -= 20
        reasons.append("MACD Bearish")

    if adx14.iloc[-1] > 25:
        score += 20
        reasons.append("Strong Trend")

    if spike.iloc[-1]:
        score += 20
        reasons.append("Volume Spike")

    if score >= 80:
        signal = "BIG BUY"

    elif score <= -80:
        signal = "BIG SELL"

    else:
        signal = "WAIT"

    confidence = min(abs(score), 100)

    return {
        "signal": signal,
        "confidence": confidence,
        "score": score,
        "price": float(df["close"].iloc[-1]),
        "trend": trend_strength(df),
        "rsi": round(float(rsi14.iloc[-1]), 2),
        "atr": round(float(atr14.iloc[-1]), 2),
        "vwap": round(float(vwap_line.iloc[-1]), 2),
        "adx": round(float(adx14.iloc[-1]), 2),
        "reasons": reasons,
    }
