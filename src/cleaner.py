# src/cleaner.py

import re
import os
from email import message_from_string, policy
from email.parser import BytesParser



def extract_headers(raw_email: str) -> dict:
    """
    Extract basic headers like From, To, Subject, and Date from a raw email string.
    """
    msg = message_from_string(raw_email, policy=policy.default)
   
    return {
        "MessageID": msg.get("Message-ID", ""),
        "From": msg.get("From", ""),
        "To": msg.get("To", ""),
        "InReplyTo": msg.get("In-Reply-To", ""),
        "Subject": msg.get("Subject", ""),
        "Date": msg.get("Date", ""),
    }

def clean_body(raw_body: str) -> str:
    """
    Remove email signatures and quoted replies from the body text.
    """
    lines = raw_body.strip().splitlines()
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()

        # Skip quoted lines
        if stripped.startswith('>'):
            continue

        # Stop at common signature marker
        if stripped == "--":
            break

        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines).strip()

def normalize_subject(subject: str) -> str:
    """
    Normalize the subject line by removing prefixes like 'Re:', 'Fwd:', etc.
    """
    if not subject:
        return ""

    # Regular expression to remove common prefixes
    cleaned = re.sub(r'^(Re|Fwd|FW)(\[\d+\])?:\s*', '', subject, flags=re.IGNORECASE)

    # Repeat in case of multiple nested prefixes (e.g. Re: Fwd: Re: Subject)
    while re.match(r'^(Re|Fwd|FW)(\[\d+\])?:\s*', cleaned, flags=re.IGNORECASE):
        cleaned = re.sub(r'^(Re|Fwd|FW)(\[\d+\])?:\s*', '', cleaned, flags=re.IGNORECASE)

    return cleaned.strip()


def is_quoted_line(line: str) -> bool:
    """
    Determine if a line in the email body is a quoted reply (starts with '>').
    """
    return line.strip().startswith(">")

def build_thread_key(subject: str, iso_date: str) -> str:
    """
    Return a consistent key for grouping emails into threads,
    based on normalized subject and date.
    """
    normalized_subject = normalize_subject(subject).lower()
    return f"{normalized_subject}::{iso_date}"


def parse_email_file(filepath: str) -> dict:
    """
    Parse a .eml file and return a cleaned representation with headers and cleaned body.
    Attachments are ignored.
    """
    with open(filepath, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    headers = {
        "From": msg.get("From", ""),
        "To": msg.get("To", ""),
        "Subject": msg.get("Subject", ""),
        "Date": msg.get("Date", ""),
    }

    # Get plain text body (ignore HTML and attachments)
    if msg.is_multipart():
        parts = [part for part in msg.walk()
                 if part.get_content_type() == 'text/plain' and not part.get_content_disposition()]
        body = parts[0].get_content().strip() if parts else ""
    else:
        body = msg.get_content().strip()

    # Clean the body using your existing function
    cleaned_body = clean_body(body)

    return {
        **headers,
        "Body": cleaned_body,
        "ThreadKey": build_thread_key(headers["Subject"], headers["Date"]),
        "Filename": os.path.basename(filepath),
    }

def parse_enron_email_string(raw_email: str, filename: str = "") -> dict:
    """
    Parse a raw Enron email string (not .eml) into cleaned fields.
    """
    headers = extract_headers(raw_email)

    # Split header and body using double newline as separator
    parts = raw_email.split("\n\n", 1)
    body = parts[1] if len(parts) > 1 else ""

    cleaned_body = clean_body(body)

    return {
        **headers,
        "Body": cleaned_body,
        "ThreadKey": build_thread_key(headers["Subject"], headers["Date"]),
        "Filename": filename,
    }