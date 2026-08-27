import json
import os

from office import store
from office import hashing


def press_seal():
    if not os.path.exists(store.book_file):
        return
    with open(store.seal_file, "w", encoding="utf-8") as f:
        f.write(hashing.file_hash(store.book_file))


def check_seal():
    if not os.path.exists(store.book_file):
        with open(store.book_file, "w", encoding="utf-8") as f:
            json.dump([], f)
        press_seal()
        return True, "200 - No ledger was on the shelf. I started a blank one."

    now_hash = hashing.file_hash(store.book_file)

    if not os.path.exists(store.seal_file):
        press_seal()
        return True, "200 - First seal pressed on the ledger."

    with open(store.seal_file, "r", encoding="utf-8") as f:
        old_hash = f.read().strip()

    if now_hash != old_hash:
        store.seal_broken = True
        return False, (
            "403 - The ledger's seal is broken. Someone has tampered with the book.\n"
            "The window will stay standing, but I will not serve parcels "
            "from a vandalised ledger."
        )

    return True, "200 - Ledger seal matches. The book is clean."
