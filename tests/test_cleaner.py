import pytest
from src.cleaner import (
    extract_headers,
    clean_body,
    normalize_subject,
    is_quoted_line,
    build_thread_key,
    parse_email_file
)

def test_extract_headers_from_email():
    """
    test extract headers from email, creates the raw email and get the headers
    """
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
    """
    removes signatures and quoted. quoted means if it's a response or forwarded email
    """
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
    """
    test removes extra Fwd and RE
    """
    subj = "Fwd: Re: RE: Urgent Request"
    cleaned = normalize_subject(subj)
    assert cleaned == "Urgent Request"

@pytest.mark.parametrize("raw, expected", [
    ("Re: Hello", "Hello"),
    ("RE: Hello", "Hello"),
    ("Fwd: Hello", "Hello"),
    ("FW: Hello", "Hello"),
    ("Fwd: Re: Hello", "Hello"),
    ("FW: RE: FWD: FW: Hello", "Hello"),
    ("Re[2]: Hello", "Hello"),
    ("Fwd[10]: Re: FW: Hello", "Hello"),
    ("No prefix here", "No prefix here"),
    ("", ""),
    (None, ""),
])
def test_normalize_subject(raw, expected):
    """
    test different normalizations
    """
    assert normalize_subject(raw) == expected

def test_is_quoted_line():
    """
    determine if the line is quoted or not
    """
    assert is_quoted_line("> Hello there!") is True
    assert is_quoted_line("This is not quoted.") is False

def test_build_thread_key_consistent():
    """
    test if the email is part of the email thread
    """
    subj = "RE: Meeting on Friday"
    date = "2001-04-05T09:30:00"
    key1 = build_thread_key(subj, date)
    key2 = build_thread_key("Fwd: Re: Meeting on Friday", date)
    assert key1 == key2

def test_parse_email_file_creates_clean_dict(tmp_path):
    """
    test the parsing can be done in eml files
    """
    # Fake raw email content
    raw_email = (
        "From: alice@example.com\n"
        "To: bob@example.com\n"
        "Subject: Re: Vacation\n"
        "Date: Mon, 12 Jun 2023 10:15:00 -0700\n"
        "Content-Type: text/plain; charset=\"UTF-8\"\n"
        "\n"
        "Hi Bob,\n\nI'd like to request some PTO.\n\n-- \nAlice"
    )

    # Write to a temp file
    email_file = tmp_path / "fake_email.eml"
    email_file.write_bytes(raw_email.encode('utf-8'))

    result = parse_email_file(str(email_file))

    assert result["From"] == "alice@example.com"
    assert result["To"] == "bob@example.com"
    assert result["Subject"] == "Re: Vacation"
    assert result["Body"] == "Hi Bob,\n\nI'd like to request some PTO."
    assert result["ThreadKey"].startswith("vacation::")
    assert result["Filename"] == "fake_email.eml"
