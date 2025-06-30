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


def test_build_thread_map_mixed_strategy():
    """
    Test build_thread_map groups emails by In-Reply-To if present,
    or falls back to subject + participants.
    """
    emails = [
        {
            "MessageID": "<1@example.com>",
            "InReplyTo": "",
            "From": "alice@example.com",
            "To": "bob@example.com",
            "Subject": "Budget Plan",
            "Date": "2023-01-01T10:00:00",
        },
        {
            "MessageID": "<2@example.com>",
            "InReplyTo": "<1@example.com>",
            "From": "bob@example.com",
            "To": "alice@example.com",
            "Subject": "Re: Budget Plan",
            "Date": "2023-01-01T11:00:00",
        },
        {
            "MessageID": "<3@example.com>",
            "InReplyTo": "",
            "From": "carol@example.com",
            "To": "dave@example.com",
            "Subject": "Holiday Plans",
            "Date": "2023-01-01T12:00:00",
        },
        {
            "MessageID": "<4@example.com>",
            "InReplyTo": "",
            "From": "dave@example.com",
            "To": "carol@example.com",
            "Subject": "Re: Holiday Plans",
            "Date": "2023-01-01T13:00:00",
        }
    ]

    thread_map = build_thread_map(emails)

    # There should be 2 threads (one via In-Reply-To, one via heuristic)
    assert len(thread_map) == 2

    thread_sizes = [len(thread) for thread in thread_map.values()]
    assert sorted(thread_sizes) == [2, 2]  # two threads of 2 emails each

    # Check that thread positions are assigned correctly
    for thread in thread_map.values():
        positions = [email["ThreadPosition"] for email in thread]
        assert sorted(positions) == [0, 1]
