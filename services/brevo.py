import os
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")


def send_emails(emails):
    print("\n[4/4] Brevo")
    print("Sending outreach emails...")

    if not BREVO_API_KEY or not SENDER_EMAIL:
        print("Brevo API key or sender email missing in .env file.")
        print("Demo mode: emails not actually sent.")

        for item in emails:
            print(f"Demo email prepared for {item['email']}")

        return

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    for item in emails:
        payload = {
            "sender": {
                "name": SENDER_NAME,
                "email": SENDER_EMAIL
            },
            "to": [
                {
                    "email": item["email"],
                    "name": item["name"]
                }
            ],
            "subject": f"Quick question for {item['company']}",
            "htmlContent": f"""
            <p>Hi {item['name']},</p>
            <p>I noticed your work at {item['company']}.</p>
            <p>I wanted to quickly connect and share a possible collaboration idea.</p>
            <p>Regards,<br>{SENDER_NAME}</p>
            """
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code in [200, 201, 202]:
            print(f"Email sent to {item['email']}")
        else:
            print(f"Failed to send to {item['email']}")
            print(response.text)