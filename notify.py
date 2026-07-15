import requests

TOPIC = "nakshatra-ai-v3"


def send_notification(title, message):

    url = f"https://ntfy.sh/{TOPIC}"

    # Emoji Title me mat bhejo
    safe_title = (
        title.replace("🟢", "")
             .replace("🔴", "")
             .replace("🚨", "")
             .replace("🔥", "")
             .strip()
    )

    headers = {
        "Title": safe_title,
        "Priority": "5",
        "Tags": "money_bag,chart_with_upwards_trend"
    }

    try:

        response = requests.post(
            url,
            data=message.encode("utf-8"),
            headers=headers,
            timeout=15
        )

        print("=" * 40)
        print("NTFY STATUS :", response.status_code)
        print("NTFY RESPONSE :", response.text)
        print("=" * 40)

        if response.status_code == 200:
            print("✅ ntfy Sent Successfully")
            return True

        print("❌ ntfy Failed")
        return False

    except Exception as e:
        print("❌ NTFY ERROR :", e)
        return False
