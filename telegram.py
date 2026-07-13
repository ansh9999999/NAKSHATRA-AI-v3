import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_message(message):

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram credentials missing")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:

        r = requests.post(url, data=payload, timeout=15)

        print("========================================")
        print("📤 Sending Telegram Message...")
        print("Status Code :", r.status_code)
        print("Response :", r.text)
        print("========================================")

        if r.status_code != 200:
            print("❌ HTTP Error")
            return False

        data = r.json()

        if data.get("ok"):

            print("✅ Telegram Sent Successfully")
            return True

        else:

            print("❌ Telegram API Error")
            print(data)
            return False

    except Exception as e:

        print("❌ Telegram Exception")
        print(e)
        return False
