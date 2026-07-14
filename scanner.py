# scanner.py

from analysis.signal import generate_signal
from telegram import send_telegram_message

# Symbols to scan
SYMBOLS = [
    "BTCUSD",
    "ETHUSD",
]


def scan_market():
    print("=" * 60)
    print("🚀 NAKSHATRA AI MARKET SCANNER STARTED")
    print("=" * 60)

    for symbol in SYMBOLS:
        try:
            print(f"\n📊 Scanning {symbol}...")

            signal = generate_signal(symbol)

            if signal is None:
                print(f"❌ No signal for {symbol}")
                continue

            send_telegram_message(signal)

            print(f"✅ {symbol} Alert Sent")

        except Exception as e:
            print(f"❌ Error scanning {symbol}")
            print(e)

    print("\n✅ Market Scan Finished")
    print("=" * 60)


if __name__ == "__main__":
    scan_market()
