import json
import os
import random
import string
import datetime

from office import store
from office import indexes
from office import seal


def open_book():
    if not os.path.exists(store.book_file):
        store.all_pages = []
        indexes.fill_notes()
        return

    try:
        with open(store.book_file, "r", encoding="utf-8") as f:
            store.all_pages = json.load(f)
    except (OSError, json.JSONDecodeError):
        store.all_pages = []

    if type(store.all_pages) is not list:
        store.all_pages = []

    indexes.fill_notes()


def save_book():
    with open(store.book_file, "w", encoding="utf-8") as f:
        json.dump(store.all_pages, f, indent=1)
    seal.press_seal()


def new_code():
    while True:
        digits = str(random.randint(1000000, 9999999))
        letters = (
            random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_uppercase)
        )
        code = "SA-" + digits + "-" + letters
        if code not in store.code_notes:
            return code


def add_parcel(details):
    code = (details.get("tracking_code") or "").strip()
    if code == "":
        code = new_code()
    if code in store.code_notes:
        return None, "400 - That tracking code is already in the ledger."

    parcel = {
        "tracking_code": code,
        "sender": details["sender"],
        "receiver": details["receiver"],
        "origin": details["origin"],
        "destination": details["destination"],
        "status": details.get("status") or "at station",
        "weight_kg": details["weight_kg"],
        "date_shipped": details.get("date_shipped")
        or datetime.date.today().isoformat(),
    }
    store.all_pages.append(parcel)
    store.code_notes[code] = parcel
    indexes.add_note(store.city_notes, parcel["destination"], code)
    indexes.add_note(store.status_notes, parcel["status"], code)
    save_book()
    return parcel, None


def set_status(code, new_status):
    parcel = indexes.find_code(code)
    if parcel is None:
        return None, None, "404 - There is no parcel " + code + "."

    old_status = parcel["status"]
    indexes.drop_note(store.status_notes, old_status, code)
    parcel["status"] = new_status
    indexes.add_note(store.status_notes, new_status, code)
    save_book()
    return parcel, old_status, None


def drop_parcel(code):
    parcel = indexes.find_code(code)
    if parcel is None:
        return None, "404 - There is no parcel " + code + "."

    store.all_pages.remove(parcel)
    del store.code_notes[code]
    indexes.drop_note(store.city_notes, parcel["destination"], code)
    indexes.drop_note(store.status_notes, parcel["status"], code)
    save_book()
    return parcel, None


def count_ask(code):
    if code not in store.ask_count:
        store.ask_count[code] = 0
    store.ask_count[code] += 1


def top_asked():
    if len(store.ask_count) == 0:
        return "200 - The most-wanted board is empty. Nobody has asked yet."

    rows = []
    for code in store.ask_count:
        rows.append([store.ask_count[code], code])
    rows.sort(reverse=True)

    lines = ["200 - Most wanted (asked about most often):"]
    rank = 1
    for row in rows[:10]:
        times = row[0]
        code = row[1]
        label = " time" if times == 1 else " times"
        lines.append("  " + str(rank) + ". " + code + " - " + str(times) + label)
        rank = rank + 1
    return "\n".join(lines)
