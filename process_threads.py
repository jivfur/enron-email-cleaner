from tqdm import tqdm
import json
from src.thread_builder import build_thread_map

def main():
    with open("../cleaned_enron_emails.json", "r", encoding="utf-8") as f:
        emails = json.load(f)

    print(f"Loaded {len(emails)} emails")

    # Show progress bar while assigning ThreadIDs (optional)
    for email in tqdm(emails, desc="Assigning thread IDs"):
        pass  # This loop can include any preprocessing if needed

    thread_map = build_thread_map(emails)  # Usually fast, no progress bar needed here

    with open("threaded_emails.json", "w", encoding="utf-8") as f:
        json.dump(thread_map, f, indent=2)

    print("Threaded emails saved.")

if __name__ == "__main__":
    main()
