# tests/test_thread_builder.py

import pytest
from src.thread_builder import build_thread_map

mock_emails = [
    {
        "MessageID": "<1@enron.com>",
        "InReplyTo": None,
        "Subject": "Lunch Plans",
        "Date": "2000-12-01T09:00:00",
        "From": "alice@enron.com",
        "To": "bob@enron.com",
    },
    {
        "MessageID": "<2@enron.com>",
        "InReplyTo": "<1@enron.com>",
        "Subject": "Re: Lunch Plans",
        "Date": "2000-12-01T09:30:00",
        "From": "bob@enron.com",
        "To": "alice@enron.com",
    },
    {
        "MessageID": "<3@enron.com>",
        "InReplyTo": "<2@enron.com>",
        "Subject": "Re: Lunch Plans",
        "Date": "2000-12-01T09:45:00",
        "From": "alice@enron.com",
        "To": "bob@enron.com",
    },
    {
        "MessageID": "<4@enron.com>",
        "InReplyTo": None,
        "Subject": "Weekend Plan",
        "Date": "2000-12-02T12:00:00",
        "From": "carol@enron.com",
        "To": "dan@enron.com",
    }
]

def test_thread_building():
    thread_map = build_thread_map(mock_emails)

    assert len(thread_map) == 2
    for thread in thread_map.values():
        dates = [email["Date"] for email in thread]
        assert dates == sorted(dates)

    # Check positions
    for thread in thread_map.values():
        for idx, email in enumerate(thread):
            assert email["ThreadPosition"] == idx
