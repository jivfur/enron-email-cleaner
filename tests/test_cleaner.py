import pytest
from src.cleaner import (
    extract_headers,
    clean_body,
    normalize_subject,
    is_quoted_line,
    build_thread_key,
)

def test_extract_headers_from_email():
    raw_email = (
        "From: alice@example.com\n"
        "To: bob@example.com\n"
        "Subject: Re: Meeting Notes\n"
        "Date: Mon, 3 Apr 2001 10:15:00 -0700\n\n"
        "Let's meet today."
    )
    headers = extract_headers(raw_email)
    assert headers['From'] == "alice@example.com"
    assert headers['To'] == "bob@example.com"
    assert headers['Subject'] == "Re: Meeting Notes"
    assert "Date" in headers

def test_clean_body_removes_signature_and_quoted():
    raw_body = (
        "Hi team,\n\n"
        "Here's the update.\n\n"
        "-- \nAlice\n\n"
        "> On Mon, Bob wrote:\n> What’s the update?"
    )
    cleaned = clean_body(raw_body)
    assert "Alice" not in cleaned
    assert "On Mon" not in cleaned
    assert "update" in cleaned

def test_normalize_subject_removes_reply_and_forward():
    subj = "Fwd: Re: RE: Urgent Request"
    cleaned = normalize_subject(subj)
    assert cleaned == "Urgent Request"

def test_is_quoted_line():
    assert is_quoted_line("> Hello there!") is True
    assert is_quoted_line("This is not quoted.") is False

def test_build_thread_key_consistent():
    subj = "RE: Meeting on Friday"
    date = "2001-04-05T09:30:00"
    key1 = build_thread_key(subj, date)
    key2 = build_thread_key("Fwd: Re: Meeting on Friday", date)
    assert key1 == key2
