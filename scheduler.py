from apscheduler.schedulers.background import BackgroundScheduler

from history import get_history
from analysis.signal import generate_signal
from telegram import send_message
from config import DEFAULT_SYMBOL

scheduler = BackgroundScheduler()

last_signal = None


def market_scan():

    global last_signal

    try:

        df = get_history(
            symbol=DEFAULT_SYMBOL,
            resolution="5m"
        )

        if df.empty:
            print("No Market Data")
            return

        signal = generate_signal(df)

        current = signal["signal"]

        if current == "WAIT":
            return

        if current == last_signal:
            return

        last_signal = current

        emoji = "🟢" if current == "BIG BUY" else "🔴"

        message = f"""
🚨 NAKSHATRA AI v3

{emoji} {current}

📊 Symbol : {DEFAULT_SYMBOL}

💰 Price : {signal['price']}

🔥 Confidence : {signal['confidence']}%

📈 Trend : {signal['trend']}

📉 RSI : {signal['rsi']}

📊 ADX : {signal['adx']}

📊 ATR : {signal['atr']}

Reasons

- {'\n- '.join(signal['reasons'])}
"""

        send_message(message)

        print("Alert Sent")

    except Exception as e:

        print(e)


def start_scheduler():

    scheduler.add_job(
        market_scan,
        "interval",
        minutes=5,
        max_instances=1
    )

    scheduler.start()

    print("Scheduler Started")

    market_scan()
