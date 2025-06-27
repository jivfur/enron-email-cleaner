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
    # Placeholder return
    return raw_body


def normalize_subject(subject: str) -> str:
    """
    Normalize the subject line by removing 'Re:', 'Fwd:', etc.
    """
    return subject


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
