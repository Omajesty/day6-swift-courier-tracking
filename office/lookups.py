import time

from office import cache
from office import indexes
from office import parcels
from office import store
from office import format as fmt


def do_get(rest_words):
    if len(rest_words) == 0:
        return "400 - GET what? Try: GET parcel <code>  or  GET parcels to <city>."

    first_word = rest_words[0].lower()

    if first_word == "most" and len(rest_words) >= 2 and rest_words[1].lower() == "wanted":
        return parcels.top_asked()

    if first_word == "parcel":
        if len(rest_words) < 2:
            return "400 - Which tracking code? Try: GET parcel SA-1234567-AB."
        return get_parcel(rest_words[1])

    if first_word == "parcels":
        return get_group(rest_words[1:])

    return fmt.BAD_SLIP


def get_group(rest_words):
    if len(rest_words) >= 1 and rest_words[0].lower() == "to":
        city = " ".join(rest_words[1:]).strip()
        if city == "":
            return "400 - Which city? Try: GET parcels to Kano."
        return get_list(
            "city",
            city,
            indexes.city_list(city),
            "There are no parcels heading to " + city + ".",
        )

    joined = " ".join(rest_words).lower()
    if joined.startswith("out for delivery"):
        return get_list(
            "status",
            "out for delivery",
            indexes.status_list("out for delivery"),
            "There are no parcels that are out for delivery.",
        )

    return (
        "400 - I cannot read this slip. Try: GET parcels to <city> "
        "or GET parcels out for delivery."
    )


def get_parcel(code):
    saved = cache.cache_get("parcel", code)
    if saved is not None:
        parcels.count_ask(code)
        return fmt.found_ms(0, saved, True)

    started = time.perf_counter()
    parcel = indexes.find_code(code)
    milliseconds = (time.perf_counter() - started) * 1000

    if parcel is None:
        return "404 - There is no parcel " + code + "."

    card = fmt.full_card(parcel)
    cache.cache_put("parcel", code, card)
    parcels.count_ask(code)
    return fmt.found_ms(milliseconds, card)


def get_list(kind, heading, codes, missing):
    saved = cache.cache_get(kind, heading)
    if saved is not None:
        parts = saved.split("\n", 1)
        body = parts[1] if len(parts) == 2 else ""
        return fmt.list_ms(parts[0], 0, body, True)

    started = time.perf_counter()
    lines = []
    for code in codes:
        lines.append(fmt.short_line(store.code_notes[code]))
    milliseconds = (time.perf_counter() - started) * 1000

    if len(lines) == 0:
        return "404 - " + missing

    shown = fmt.clip_list(lines)
    count_text = "{:,}".format(len(lines)) + " parcels found"
    cache.cache_put(kind, heading, count_text + "\n" + shown)
    return fmt.list_ms(count_text, milliseconds, shown)
