import os
import requests
from dotenv import load_dotenv

load_dotenv()

PROSPEO_API_KEY = os.getenv("PROSPEO_API_KEY")


def get_decision_makers(companies):
    print("\n[2/4] Prospeo")
    print("Finding decision makers...")

    if not PROSPEO_API_KEY:
        print("Prospeo API key missing. Using demo data.")
        return [
            {
                "person_id": "",
                "name": "Pavan V",
                "role": "Software Engineer",
                "company": companies[0],
                "linkedin": "https://linkedin.com/in/pavanv"
            }
        ]

    url = "https://api.prospeo.io/search-person"

    headers = {
        "X-KEY": PROSPEO_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "page": 1,
        "filters": {
            "company": {
                "websites": {
                    "include": companies
                }
            }
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)

        if response.status_code != 200:
            print("Prospeo API failed.")
            print(response.text)
            return []

        data = response.json()
        contacts = []

        for result in data.get("results", []):
            person = result.get("person", {})
            company = result.get("company", {})

            contacts.append({
                "person_id": person.get("person_id", ""),
                "name": person.get("full_name", "Unknown"),
                "role": person.get("current_job_title", "Unknown"),
                "company": company.get("website", ""),
                "linkedin": person.get("linkedin_url", "")
            })

        # Limit contacts for demo to avoid too many enrich API calls
        return contacts[:5]

    except requests.exceptions.RequestException as error:
        print(f"Network error while calling Prospeo: {error}")
        return []