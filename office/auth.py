import json
import os

from office import store
from office import hashing
from office import tokens

first_staff = [
    {"username": "oga_musty", "password": "stationmaster1",
    "position": "Station Master", "name": "Musty"},
    {"username": "kemi_dispatch", "password": "parcels4kemi",
    "position": "Clerk", "name": "Kemi"},
    {"username": "ibrahim_k", "password": "fastdelivery",
    "position": "Clerk", "name": "Ibrahim"},
    {"username": "ngozi_front", "password": "deskt2026",
    "position": "Clerk", "name": "Ngozi"},
]

dead_tokens = set()

def open_staff():
    """Open the staff file and return the data as a list of dictionaries."""
    if os.path.exists(store.staff_file):
        with open(store.staff_file, "r", encoding="utf-8") as f:
            staff_book = json.load(f)
        first = list(staff_book.values())[0] if staff_book else {}
        if "salt" in first:
            return staff_book
    
    staff_book = {}
    for person in first_staff:
        salt = hashing.make_salt()
        staff_book[person["username"]] = {
            "salt": salt,
            "pass_hash": hashing.hash_pass(person["password"], salt),
            "position": person["position"],
            "name": person["name"],
            }
    with open(store.staff_file, "w", encoding="utf-8") as f:
        json.dump(staff_book, f, indent=2)
    return staff_book

def sign_in(username, password, staff_book):
    """Sign in a user by checking their username and password."""
    if username not in staff_book:
        return "401 - I do not know that username.", None
    
    person = staff_book[username]
    typed_hash = hashing.hash_pass(password, person["salt"])
    if typed_hash != person["pass_hash"]:
        return "401 - That password does not match.", None
    
    info = {"username": username, "position": person["position"], "name": person["name"],}
    
    day_pass = tokens.make_jwt(info)
    reply = (
        "200 - Welcome," + info["name"] + " (" + info["position"] + "). \n"
        "Your day pass is: " + day_pass + "\n"
        "(Show this pass with every slip. It expires in 5 minutes.)"
    )
    return reply, day_pass

def check_pass(day_pass):
    """Check if a day pass is valid and return the user info if it is."""
    if day_pass is None or day_pass =="":
        return None, "401 - No day pass on this slip. Please sign in."
    if day_pass in dead_tokens:
        return None, tokens.bad_token
    return tokens.read_jwt(day_pass)

def drop_pass(day_pass):
    """Invalidate a day pass by adding it to the dead tokens set."""
    person, error = tokens.read_jwt(day_pass)
    if error is not None:
        return error
    dead_tokens.add(day_pass)
    return "200 - Day pass destroyed. Please sign in again to get a new one."

def is_master(person):
    """Check if the person is a Station Master."""
    return person["position"] == "Station Master"