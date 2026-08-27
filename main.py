from office import auth
from office import parcels
from office import handlers
from office import seal
from office import store


def show_board():
    print("==============================================")
    print("SWIFT ARROW COURIERS - TRACKING WINDOW")
    print("==============================================")


def show_menu():
    print("--------- WINDOW MENU ---------")
    print("1. GET parcel <code> - track one parcel")
    print("2. GET parcels to <city> - all parcels heading to a city")
    print("3. POST parcel - register a new parcel")
    print("4. PUT parcel <code> - update a parcel")
    print("5. DELETE parcel <code> - remove a parcel (Station Master only)")
    print("6. GET most wanted - the ten codes asked about most")
    print("7. GET parcels out for delivery")
    print("8. Sign out")
    print("9. Close the window")
    print("-------------------------------")
    print("Type the full slip (recommended), including your day pass:")
    print("  <your pass> GET parcel SA-1998500-IY")
    print("Or type a number, and I will ask for the missing pieces.")


def ask_login(staff_book):
    print()
    print("--- sign in first ---")
    while True:
        username = input("Username: ").strip()
        if username.lower() in ("q", "quit", "close", "9"):
            return None
        password = input("Password: ").strip()
        reply, day_pass = auth.sign_in(username, password, staff_book)
        print(reply)
        if day_pass is not None:
            return day_pass
        print("(Try again, or type 'close' as the username to leave.)")


def menu_slip(choice, day_pass):
    if choice == "1":
        code = input("Tracking code: ").strip()
        return day_pass + " GET parcel " + code
    if choice == "2":
        city = input("City: ").strip()
        return day_pass + " GET parcels to " + city
    if choice == "3":
        return day_pass + " POST parcel"
    if choice == "4":
        code = input("Tracking code: ").strip()
        return day_pass + " PUT parcel " + code
    if choice == "5":
        code = input("Tracking code: ").strip()
        return day_pass + " DELETE parcel " + code
    if choice == "6":
        return day_pass + " GET most wanted"
    if choice == "7":
        return day_pass + " GET parcels out for delivery"
    return None


def take_slips(day_pass):
    while True:
        print()
        show_menu()
        typed_line = input("Pass slip: ").strip()

        if typed_line == "":
            print("400 - Empty slip.")
            continue

        first_word = typed_line.split()[0]

        if first_word == "9" or typed_line.lower() in ("close", "quit", "exit"):
            return "close"

        if first_word == "8" or typed_line.lower() in ("sign out", "signout"):
            print(auth.drop_pass(day_pass))
            return "signed out"

        if first_word in ("1", "2", "3", "4", "5", "6", "7"):
            slip = menu_slip(first_word, day_pass)
            if slip is None:
                print("400 - I cannot read this slip. The verbs are GET, POST, PUT, DELETE.")
                continue
        else:
            slip = typed_line
            known_verbs = ("GET", "POST", "PUT", "DELETE", "SIGN")
            if first_word.upper() in known_verbs:
                slip = day_pass + " " + typed_line

        reply = handlers.read_slip(slip)
        print(reply)

        if reply.startswith("401 - Your day pass has expired"):
            return "expired"
        if reply.startswith("200 - Day pass destroyed"):
            return "signed out"


def open_window():
    show_board()

    staff_book = auth.open_staff()

    seal_ok, seal_text = seal.check_seal()
    print(seal_text)
    if not seal_ok:
        print()
        print("Type anything and press Enter to close.")
        input()
        return

    parcels.open_book()
    print(
        "200 - Ledger loaded. Notebooks ready. "
        + "{:,}".format(len(store.all_pages))
        + " parcels on the shelf."
    )

    while True:
        day_pass = ask_login(staff_book)
        if day_pass is None:
            print("200 - Window closed. Go well.")
            return

        loop_end = take_slips(day_pass)
        if loop_end == "close":
            print("200 - Window closed. Go well.")
            return


if __name__ == "__main__":
    open_window()
