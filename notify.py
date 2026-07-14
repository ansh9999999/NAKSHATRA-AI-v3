import requests

TOPIC = "nakshatra-ai-v3"

def send_notification(title, message):

    url = f"https://ntfy.sh/{TOPIC}"

    headers = {
        "Title": title,
        "Priority": "5",
        "Tags": "chart_with_upwards_trend,money_bag"
    }

    requests.post(
        url,
        data=message.encode("utf-8"),
        headers=headers,
        timeout=10
    )


if __name__ == "__main__":

    send_notification(
        "🚀 NAKSHATRA AI",
        "Congratulations!\n\nYour ntfy notification is working."
    )
