from office import auth
from office import lookups
from office import writes
from office import store
from office import format as fmt


def read_slip(slip_text):
    if store.seal_broken:
        return (
            "403 - The ledger's seal is broken. I will not open a tampered book.\n"
            "The window remains standing."
        )

    slip_text = slip_text.strip()
    if slip_text == "":
        return "400 - Empty slip."

    words = slip_text.split()
    day_pass = words[0]
    request = words[1:]

    if len(request) >= 1 and request[0].upper() == "SIGNOUT":
        return auth.drop_pass(day_pass)
    if len(request) >= 2 and request[0].upper() == "SIGN" and request[1].upper() == "OUT":
        return auth.drop_pass(day_pass)

    person, error = auth.check_pass(day_pass)
    if error is not None:
        return error

    if len(request) == 0:
        return fmt.BAD_SLIP

    verb = request[0].upper()
    rest_words = request[1:]

    if verb == "GET":
        return lookups.do_get(rest_words)
    if verb == "POST":
        return writes.do_post(rest_words)
    if verb == "PUT":
        return writes.do_put(rest_words)
    if verb == "DELETE":
        return writes.do_delete(rest_words, person)

    return fmt.BAD_SLIP
