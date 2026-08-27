from office import auth
from office import cache
from office import indexes
from office import parcels
from office import store
from office import format as fmt


def do_post(rest_words):
    if len(rest_words) >= 1 and rest_words[0].lower() != "parcel":
        return "400 - To register a parcel, the slip is: POST parcel."

    print("  (Ask for the new parcel's details.)")
    code = input("  Tracking code (press Enter to invent one): ").strip()
    sender = input("  Sender: ").strip()
    receiver = input("  Receiver: ").strip()
    origin = input("  Origin city: ").strip()
    destination = input("  Destination city: ").strip()
    status = input("  Status [at station]: ").strip() or "at station"
    weight_text = input("  Weight in kg: ").strip()

    if sender == "" or receiver == "" or origin == "" or destination == "":
        return "400 - Sender, receiver, origin and destination are required."

    try:
        weight = float(weight_text)
    except ValueError:
        return "400 - Weight must be a number, for example 12.4."

    parcel, error = parcels.add_parcel({
        "tracking_code": code,
        "sender": sender,
        "receiver": receiver,
        "origin": origin,
        "destination": destination,
        "status": status,
        "weight_kg": weight,
    })
    if error is not None:
        return error

    cache.cache_wipe(parcel["tracking_code"], parcel["destination"], parcel["status"])
    return "201 - Parcel registered.\n" + fmt.full_card(parcel)


def do_put(rest_words):
    if len(rest_words) < 2 or rest_words[0].lower() != "parcel":
        return "400 - To update a parcel, the slip is: PUT parcel <code>."

    code = rest_words[1]
    parcel = indexes.find_code(code)
    if parcel is None:
        return "404 - There is no parcel " + code + "."

    print("  Current status: " + parcel["status"])
    new_status = input(
        "  New status (at station / in transit / out for delivery / delivered): "
    ).strip()
    if new_status == "":
        return "400 - I need a new status."

    city = parcel["destination"]
    parcel, old_status, error = parcels.set_status(code, new_status)
    if error is not None:
        return error

    cache.cache_wipe(code, city, parcel["status"], old_status)
    return "200 - Parcel updated.\n" + fmt.full_card(parcel)


def do_delete(rest_words, person):
    if not auth.is_master(person):
        return "403 - Clerks may not delete parcels. Speak to the Station Master."

    if len(rest_words) < 2 or rest_words[0].lower() != "parcel":
        return "400 - To remove a parcel, the slip is: DELETE parcel <code>."

    code = rest_words[1]
    parcel = indexes.find_code(code)
    if parcel is None:
        return "404 - There is no parcel " + code + "."

    city = parcel["destination"]
    status = parcel["status"]
    parcel, error = parcels.drop_parcel(code)
    if error is not None:
        return error

    cache.cache_wipe(code, city, status)
    if code in store.ask_count:
        del store.ask_count[code]
    return (
        "200 - Parcel "
        + parcel["tracking_code"]
        + " is gone from the ledger, the notebooks, and the tray."
    )
