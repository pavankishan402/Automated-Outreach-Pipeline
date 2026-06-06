from services.ocean import find_similar_companies
from services.prospeo import get_decision_makers
from services.eazyreach import resolve_emails
from services.brevo import send_emails


def main():
    print("=" * 50)
    print("AUTOMATED OUTREACH PIPELINE")
    print("=" * 50)

    domain = input("Enter company domain: ")

    companies = find_similar_companies(domain)

    print("\nSimilar Companies Found:")
    for company in companies:
        print(f" - {company}")

    contacts = get_decision_makers(companies)

    print("\nDecision Makers Found:")
    for contact in contacts:
        print(f"Name: {contact['name']}")
        print(f"Role: {contact['role']}")
        print(f"Company: {contact['company']}")
        print(f"LinkedIn: {contact['linkedin']}")
        print("-" * 30)

    emails = resolve_emails(contacts)

    print("\nVerified Emails:")
    for item in emails:
        print(f"Name: {item['name']}")
        print(f"Role: {item['role']}")
        print(f"Company: {item['company']}")
        print(f"LinkedIn: {item['linkedin']}")
        print(f"Email: {item['email']}")
        print(f"Status: {item['status']}")
        print("-" * 30)

    print("\nSummary")
    print("=" * 30)
    print(f"Total Companies: {len(companies)}")
    print(f"Total Contacts: {len(contacts)}")
    print(f"Total Emails: {len(emails)}")

    choice = input("\nSend emails now? (yes/no): ")

    if choice.lower() == "yes":
        send_emails(emails)
    else:
        print("Email sending cancelled.")


if __name__ == "__main__":
    main()