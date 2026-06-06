def find_similar_companies(domain):
    print("\n[1/4] Ocean.io")
    print(f"Finding companies similar to {domain}")

    return [
        "freshworks.com",
        "hubspot.com",
        "salesforce.com"
    ]
def get_decision_makers(companies):
    print("\n[2/4] Prospeo")
    print("Finding decision makers...")

    return [
        {
            "name": "Pavan V",
            "role": "Software Engineer",
            "company": companies[0],
            "linkedin": "https://linkedin.com/in/pavanv"
        }
    ]