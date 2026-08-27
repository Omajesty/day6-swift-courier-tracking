import hmac
import hashlib
import json
import base64
import time

jwt_key = b"swift-arrow-jwt-secret"
pass_limit = 5 * 60
bad_token = "401 - I do not recognise this day pass."
old_token = "401 - Your day pass has expired. Please sign in again at the grille."


def b64_pack(raw_bytes):
    return base64.urlsafe_b64encode(raw_bytes).decode("utf-8").rstrip("=")


def b64_load(text):
    pad = "=" * ((4 - len(text) % 4) % 4)
    return base64.urlsafe_b64decode(text + pad)


def make_jwt(person):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "username": person["username"],
        "position": person["position"],
        "name": person["name"],
        "exp": time.time() + pass_limit,
    }
    header_b64 = b64_pack(json.dumps(header).encode("utf-8"))
    payload_b64 = b64_pack(json.dumps(payload).encode("utf-8"))
    message = header_b64 + "." + payload_b64
    sig_bytes = hmac.new(jwt_key, message.encode("utf-8"), hashlib.sha256).digest()
    return message + "." + b64_pack(sig_bytes)


def read_jwt(token):
    parts = token.split(".")
    if len(parts) != 3:
        return None, bad_token

    message = parts[0] + "." + parts[1]
    good_sig = hmac.new(jwt_key, message.encode("utf-8"), hashlib.sha256).digest()
    try:
        got_sig = b64_load(parts[2])
        payload = json.loads(b64_load(parts[1]).decode("utf-8"))
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return None, bad_token

    if not hmac.compare_digest(good_sig, got_sig):
        return None, bad_token
    if time.time() > payload["exp"]:
        return None, old_token

    person = {
        "username": payload["username"],
        "position": payload["position"],
        "name": payload["name"],
    }
    return person, None
