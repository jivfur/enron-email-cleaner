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



def test_thread_email_date_sorting():
    emails = [
        {
            "MessageID": "<19171686.1075857585034.JavaMail.evans@thyme>",
            "InReplyTo": "",
            "From": "slafontaine@globalp.com",
            "To": "john.arnold@enron.com",
            "Subject": "re:summer inverses",
            "Date": "Fri, 08 Dec 2000 05:05:00 -0800",
            "Body": "Body 1"
        },
        {
            "MessageID": "<23987417.1075857585124.JavaMail.evans@thyme>",
            "InReplyTo": "",
            "From": "slafontaine@globalp.com",
            "To": "john.arnold@enron.com",
            "Subject": "re:summer inverses",
            "Date": "Thu, 07 Dec 2000 01:27:00 -0800",
            "Body": "Body 2"
        },
        {
            "MessageID": "<16522398.1075857584074.JavaMail.evans@thyme>",
            "InReplyTo": "",
            "From": "john.arnold@enron.com",
            "To": "slafontaine@globalp.com",
            "Subject": "re:summer inverses",
            "Date": "Mon, 11 Dec 2000 09:04:00 -0800",
            "Body": "Body 3"
        },
        {
            "MessageID": "<3552781.1075857584209.JavaMail.evans@thyme>",
            "InReplyTo": "",
            "From": "john.arnold@enron.com",
            "To": "slafontaine@globalp.com",
            "Subject": "re:summer inverses",
            "Date": "Mon, 11 Dec 2000 08:51:00 -0800",
            "Body": "Body 4"
        },
        {
            "MessageID": "<17938862.1075857585990.JavaMail.evans@thyme>",
            "InReplyTo": "",
            "From": "john.arnold@enron.com",
            "To": "slafontaine@globalp.com",
            "Subject": "re:summer inverses",
            "Date": "Wed, 06 Dec 2000 21:38:00 -0800",
            "Body": "Body 5"
        }
    ]

    thread_map = build_thread_map(emails)
    # Extract the thread (only one thread expected)
    threads = list(thread_map.values())
    assert len(threads) == 1, "Expected exactly one thread"

    thread_emails = threads[0]
    # Dates extracted from the sorted thread
    dates = [email["Date"] for email in thread_emails]
    print(dates)
    expected_order = [
        "Wed, 06 Dec 2000 21:38:00 -0800",
        "Thu, 07 Dec 2000 01:27:00 -0800",
        "Fri, 08 Dec 2000 05:05:00 -0800",
        "Mon, 11 Dec 2000 08:51:00 -0800",
        "Mon, 11 Dec 2000 09:04:00 -0800"
    ]

    assert dates == expected_order, "Emails are not sorted correctly by Date"
    
    # Check ThreadPosition are sequential 0..n-1
    positions = [email["ThreadPosition"] for email in thread_emails]
    assert positions == list(range(len(thread_emails))), "ThreadPosition not assigned correctly"
