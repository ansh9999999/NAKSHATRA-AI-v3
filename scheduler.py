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

    print(f"🔍 Scanning {symbol}")

    df = get_history(symbol=symbol)

    if df.empty:
        print(f"❌ {symbol} : No Data")
        return

    print(df.tail())

    result = generate_signal(df)

    signal = result["signal"]

    print(f"Signal = {signal}")

    if signal == "WAIT":
        print(f"{symbol} WAIT")
        return

    if last_alerts.get(symbol) == signal:
        print(f"{symbol} Duplicate Alert")
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

📉 RSI : {result['rsi']}

📊 ADX : {result['adx']}

📊 ATR : {result['atr']}

Reasons

{chr(10).join('✅ ' + r for r in result['reasons'])}
"""

    ok = send_message(message)

    if ok:
        print(f"✅ {symbol} Alert Sent")
    else:
        print(f"❌ Telegram Failed")


def market_scan():

    print("🔄 Market Scan Started")

    for symbol in SYMBOLS:
        scan_symbol(symbol)

    print("✅ Market Scan Finished")


def start_scheduler():

    scheduler.add_job(
        market_scan,
        "interval",
        minutes=5,
        max_instances=1,
        coalesce=True
    )

    scheduler.start()

    print("🚀 Scheduler Started")

    market_scan()
