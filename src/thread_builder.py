import uuid
import hashlib
from collections import defaultdict
from datetime import datetime,timezone
from typing import List, Dict
from tqdm import tqdm

from email.utils import parsedate_to_datetime
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
    for email in tqdm(emails, desc="Building thread map Second Round"):
        # Skip emails missing any essential header
        if not all(email.get(field) for field in ["From", "To", "Subject", "Date"]):
            continue
        thread_id = thread_ids.get(email.get("MessageID"))
        email["ThreadID"] = thread_id
        thread_map[thread_id].append(email)

    # Sort and assign ThreadPosition
    print("HERE")
    for thread in thread_map.values():
        thread.sort(key=lambda e: _safe_date_parse(e.get("Date")))
        for i, email in enumerate(thread):
            email["ThreadPosition"] = i
    
    return (deduplicate_threads(thread_map))


def _safe_date_parse(date_str: str) -> datetime:
    try:
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    except Exception as e:
        print(f"Error: {e}")
        return datetime.min
 
def hash_email(email: dict) -> str:
    """
    creates the hash for the email
    """
    key_str = f"{email.get('From','')}|{email.get('To','')}|{email.get('Subject','')}|{email.get('Date','')}|{email.get('Body','')}"
    return hashlib.sha256(key_str.encode('utf-8')).hexdigest()

def deduplicate_threads(thread_map: dict) -> dict:
    """
    remove the repeated emails
    """
    cleaned_thread_map = {}
    for thread_id, emails in thread_map.items():
        seen_hashes = set()
        unique_emails = []
        for email in emails:
            h = hash_email(email)
            if h not in seen_hashes:
                seen_hashes.add(h)
                unique_emails.append(email)
        cleaned_thread_map[thread_id] = unique_emails
    return cleaned_thread_map
