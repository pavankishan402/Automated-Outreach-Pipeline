import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

PROSPEO_API_KEY = os.getenv("PROSPEO_API_KEY")


def resolve_emails(contacts):
    print("\n[3/4] Prospeo Enrich Person")
    print("Resolving verified work emails...")

    if not PROSPEO_API_KEY:
        print("Prospeo API key missing. Using demo email.")
        return [
            {
                **contact,
                "email": "pavan@example.com",
                "status": "demo"
            }
            for contact in contacts[:2]
        ]

    url = "https://api.prospeo.io/enrich-person"

    headers = {
        "X-KEY": PROSPEO_API_KEY,
        "Content-Type": "application/json"
    }

    enriched_contacts = []

    # Limit to first 2 contacts to avoid rate limit and credit usage
    for contact in contacts[:2]:
        person_id = contact.get("person_id")

        if not person_id:
            enriched_contacts.append({
                **contact,
                "email": "",
                "status": "missing_person_id"
            })
            continue

        payload = {
            "only_verified_email": True,
            "data": {
                "person_id": person_id
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=20)

            if response.status_code == 429:
                print("Rate limit hit. Waiting 5 seconds...")
                time.sleep(5)
                response = requests.post(url, json=payload, headers=headers, timeout=20)

            if response.status_code != 200:
                print(f"Could not enrich {contact.get('name')}")
                print(response.text)
                enriched_contacts.append({
                    **contact,
                    "email": "",
                    "status": "not_found"
                })
                continue

            data = response.json()
            person = data.get("person", {})
            email_data = person.get("email") or {}

            enriched_contacts.append({
                **contact,
                "email": email_data.get("email", ""),
                "status": email_data.get("status", "not_found")
            })

        except requests.exceptions.RequestException as error:
            print(f"Network error for {contact.get('name')}: {error}")
            enriched_contacts.append({
                **contact,
                "email": "",
                "status": "network_error"
            })

    return enriched_contacts