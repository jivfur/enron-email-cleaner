# src/cleaner.py

import re
from datetime import datetime
from email import message_from_string, policy


def extract_headers(raw_email: str) -> dict:
    """
    Extract basic headers like From, To, Subject, and Date from a raw email string.
    """
    msg = message_from_string(raw_email, policy=policy.default)
   
    return {
        "From": msg.get("From", ""),
        "To": msg.get("To", ""),
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
    return False


def build_thread_key(subject: str, iso_date: str) -> str:
    """
    Return a consistent key for grouping emails into threads, based on subject and date.
    """
    return f"{subject.lower()}::{iso_date}"
