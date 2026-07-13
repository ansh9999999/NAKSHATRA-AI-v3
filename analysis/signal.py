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

    # EMA
    ema9 = ema(df, 9).iloc[-1]
    ema21 = ema(df, 21).iloc[-1]

    bullish = ema9 > ema21
    bearish = ema9 < ema21

    if bullish:
        score += 20
        reasons.append("EMA Bullish")

    if bearish:
        score -= 20
        reasons.append("EMA Bearish")

    # RSI
    rsi14 = rsi(df).iloc[-1]

    if bullish and 58 <= rsi14 <= 72:
        score += 15
        reasons.append("Healthy RSI")

    elif bearish and 28 <= rsi14 <= 42:
        score -= 15
        reasons.append("Weak RSI")

    # MACD
    macd_line, signal_line, hist = macd(df)

    if macd_line.iloc[-1] > signal_line.iloc[-1]:
        score += 15
        reasons.append("MACD Bullish")
    else:
        score -= 15
        reasons.append("MACD Bearish")

    # ADX
    adx14 = adx(df).iloc[-1]

    if adx14 > 25:
        if bullish:
            score += 10
        elif bearish:
            score -= 10

        reasons.append("Strong Trend")

    # ATR
    atr14 = atr(df).iloc[-1]
    atr_avg = atr(df).tail(20).mean()

    if atr14 > atr_avg:
        if bullish:
            score += 10
        elif bearish:
            score -= 10

        reasons.append("ATR Expansion")

    # Volume
    if volume_spike(df).iloc[-1]:
        if bullish:
            score += 15
        elif bearish:
            score -= 15

        reasons.append("Volume Spike")

    # Breakout
    high20 = df["high"].tail(20).max()
    low20 = df["low"].tail(20).min()

    if bullish and price >= high20:
        score += 15
        reasons.append("Resistance Breakout")

    if bearish and price <= low20:
        score -= 15
        reasons.append("Support Breakdown")

    # Final Signal
    if score >= 40:
        signal = "BIG BUY"

    elif score <= -40:
        signal = "BIG SELL"

    else:
        signal = "WAIT"

    # Debug Output
    print("=" * 60)
    print(f"PRICE      : {price}")
    print(f"EMA9       : {ema9}")
    print(f"EMA21      : {ema21}")
    print(f"RSI        : {rsi14}")
    print(f"ADX        : {adx14}")
    print(f"ATR        : {atr14}")
    print(f"SCORE      : {score}")
    print(f"REASONS    : {reasons}")
    print(f"SIGNAL     : {signal}")
    print("=" * 60)

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
        "reasons": reasons,
        }
