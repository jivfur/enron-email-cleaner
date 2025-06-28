import os
import json
from tqdm import tqdm
from src.cleaner import parse_enron_email_string

def process_enron_folder(folder_path: str) -> list:
    """
    Walk through a folder of raw Enron email files and parse them into a list of cleaned emails.
    """
    cleaned_emails = []

    for root, _, files in os.walk(folder_path):
        for fname in tqdm(files, desc="Processing emails"):
            # if not fname.endswith(".txt"):
            #     continue

            full_path = os.path.join(root, fname)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    raw_email = f.read()
                    parsed = parse_enron_email_string(raw_email, filename=fname)
                    cleaned_emails.append(parsed)
            except Exception as e:
                print(f"Error processing {fname}: {e}")

    return cleaned_emails




emails = process_enron_folder("/maildir/")

# Optionally save as JSON
with open("cleaned_enron_emails.json", "w", encoding="utf-8") as f:
    json.dump(emails, f, indent=2)
