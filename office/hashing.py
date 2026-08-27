import hashlib
import secrets


def make_salt():
    return secrets.token_hex(16)


def hash_pass(password, salt):
    mixed = salt + password
    return hashlib.sha256(mixed.encode("utf-8")).hexdigest()


def make_hash(raw_bytes):
    return hashlib.sha256(raw_bytes).hexdigest()


def file_hash(path):
    with open(path, "rb") as f:
        return make_hash(f.read())
