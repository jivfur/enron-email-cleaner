# src/thread_builder.py

import uuid
from typing import List, Dict
from collections import defaultdict
from datetime import datetime


def build_thread_map(emails: List[dict]) -> Dict[str, List[dict]]:
    """
    Group emails into threads based on 'Message-ID' and 'In-Reply-To' headers.
    Returns a dictionary mapping ThreadIDs to lists of emails sorted chronologically.
    """
    id_lookup = {email["MessageID"]: email for email in emails if email.get("MessageID")}
    thread_map = defaultdict(list)

    for email in emails:
        current_id = email.get("MessageID")
        parent_id = email.get("InReplyTo")

        root_id = current_id
        visited = set()

        while parent_id and parent_id in id_lookup and parent_id not in visited:
            visited.add(parent_id)
            root_id = parent_id
            parent_id = id_lookup[parent_id].get("InReplyTo")

        thread_id = f"thread-{root_id}" if root_id else f"thread-{uuid.uuid4()}"
        email["ThreadID"] = thread_id
        thread_map[thread_id].append(email)

    # Sort emails in each thread by date and assign position
    for thread in thread_map.values():
        thread.sort(key=lambda e: _safe_date_parse(e.get("Date")))
        for i, email in enumerate(thread):
            email["ThreadPosition"] = i

    return thread_map


def _safe_date_parse(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        return datetime.min
