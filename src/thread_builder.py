import uuid
from collections import defaultdict
from datetime import datetime
from typing import List, Dict
from tqdm import tqdm

from src.cleaner import normalize_subject  # Assumes normalize_subject is available

def build_thread_map(emails: List[dict]) -> Dict[str, List[dict]]:
    """
    Group emails into threads using In-Reply-To headers when possible.
    Falls back to subject/participants heuristics otherwise.
    Ensures that replies and their parent messages share the same ThreadID.
    """
    id_lookup = {e["MessageID"]: e for e in emails if e.get("MessageID")}
    thread_ids = {}
    heuristic_threads = {}
    thread_map = defaultdict(list)

    def resolve_root_and_assign_chain(email):
        """
        Traverse reply chain and assign a common thread ID to all.
        """
        chain = []
        current = email

        while current:
            chain.append(current)
            in_reply_to = current.get("InReplyTo")
            if in_reply_to and in_reply_to in id_lookup:
                current = id_lookup[in_reply_to]
            else:
                current = None

        root = chain[-1]
        thread_id = f"thread-{root.get('MessageID') or uuid.uuid4()}"

        for e in chain:
            thread_ids[e["MessageID"]] = thread_id

    # First pass: assign thread IDs via In-Reply-To
    for email in tqdm(emails, desc="Building thread map"):
        # Skip emails missing any essential header
        if not all(email.get(field) for field in ["From", "To", "Subject", "Date"]):
            continue

        msg_id = email.get("MessageID")
        if msg_id in thread_ids:
            continue  # already handled in a chain
        in_reply_to = email.get("InReplyTo")

        if in_reply_to and in_reply_to in id_lookup:
            resolve_root_and_assign_chain(email)
        else:
            # Fallback: heuristic
            norm_subj = normalize_subject(email.get("Subject", ""))
            participants = tuple(sorted([
                email.get("From", "").lower(),
                email.get("To", "").lower()
            ]))
            key = (norm_subj, participants)
            if key not in heuristic_threads:
                heuristic_threads[key] = f"thread-{uuid.uuid4()}"
            thread_ids[msg_id] = heuristic_threads[key]

    # Second pass: assign and group
    for email in emails:
        thread_id = thread_ids.get(email.get("MessageID"))
        email["ThreadID"] = thread_id
        thread_map[thread_id].append(email)

    # Sort and assign ThreadPosition
    for thread in thread_map.values():
        thread.sort(key=lambda e: _safe_date_parse(e.get("Date")))
        for i, email in enumerate(thread):
            email["ThreadPosition"] = i
    return thread_map


def _safe_date_parse(date_str: str):
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        return datetime.min
