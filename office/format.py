BAD_SLIP = "400 - I cannot read this slip. The verbs are GET, POST, PUT, DELETE."


def time_ms(milliseconds):
    if milliseconds < 1:
        return "{:.3f}".format(milliseconds)
    return "{:.1f}".format(milliseconds)


def full_card(parcel):
    line1 = (
        parcel["tracking_code"] + " | "
        + parcel["sender"] + " -> " + parcel["receiver"]
    )
    line2 = (
        parcel["origin"] + " -> " + parcel["destination"]
        + " | " + parcel["status"]
        + " | " + str(parcel["weight_kg"]) + " kg"
        + " | shipped " + parcel["date_shipped"]
    )
    return line1 + "\n" + line2


def short_line(parcel):
    return (
        parcel["tracking_code"] + " | "
        + parcel["sender"] + " -> " + parcel["receiver"]
        + " | " + parcel["status"]
    )


def clip_list(lines):
    show_max = 12
    if len(lines) <= show_max:
        return "\n".join(lines)
    leftover = len(lines) - show_max
    return (
        "\n".join(lines[:show_max])
        + "\n... ("
        + "{:,}".format(leftover)
        + " more)"
    )


def found_ms(milliseconds, body, from_cache=False):
    extra = " (from the tray)" if from_cache else ""
    return "200 - Found in " + time_ms(milliseconds) + " ms" + extra + "\n" + body


def list_ms(count_text, milliseconds, body, from_cache=False):
    extra = " (from the tray)" if from_cache else ""
    return (
        "200 - "
        + count_text
        + " in "
        + time_ms(milliseconds)
        + " ms"
        + extra
        + "\n"
        + body
    )
