from apscheduler.schedulers.background import BackgroundScheduler

from history import get_history
from analysis.signal import generate_signal
from telegram import send_message

SYMBOLS = [
    "BTCUSD",
    "ETHUSD"
]

scheduler = BackgroundScheduler()

last_alerts = {}


def scan_symbol(symbol):

    df = get_history(symbol=symbol)

    if df.empty:
        print(f"{symbol} : No Data")
        return

    result = generate_signal(df)

    signal = result["signal"]

    if signal == "WAIT":
        return

    if last_alerts.get(symbol) == signal:
        return

    last_alerts[symbol] = signal

    emoji = "🟢" if signal == "BIG BUY" else "🔴"

    message = f"""
🚨 NAKSHATRA AI v3

{emoji} {signal}

📊 Symbol : {symbol}

💰 Price : {result['price']}

🔥 Confidence : {result['confidence']}%

📈 Trend : {result['trend']}

Reasons

{chr(10).join('✅ ' + r for r in result['reasons'])}
"""

    send_message(message)

    print(f"{symbol} Alert Sent")


def market_scan():

    for symbol in SYMBOLS:

        scan_symbol(symbol)


def start_scheduler():

    scheduler.add_job(
        market_scan,
        "interval",
        minutes=5,
        max_instances=1
    )

    scheduler.start()

    print("🚀 Scheduler Started")

    market_scan()
