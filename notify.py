import requests

TOPIC = "nakshatra-ai-v3"


def send_notification(title, message):

    url = f"https://ntfy.sh/{TOPIC}"

    headers = {
        "Title": title,
        "Priority": "5",
        "Tags": "money_bag,chart_with_upwards_trend"
    }

    try:
        r = requests.post(
            url,
            data=message.encode("utf-8"),
            headers=headers,
            timeout=15
        )

        print("NTFY STATUS :", r.status_code)
        print("NTFY RESPONSE :", r.text)

        return r.status_code == 200

    except Exception as e:
        print("NTFY ERROR :", e)
        return False
