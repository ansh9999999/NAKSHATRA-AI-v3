from analysis.indicators import ema, rsi


def generate_signal(df):
    return {
        "signal": "WAIT",
        "confidence": 0,
        "reason": []
    }
