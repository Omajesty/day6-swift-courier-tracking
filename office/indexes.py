from office import store


def add_note(notebook, heading, code):
    heading = heading.lower()
    if heading not in notebook:
        notebook[heading] = []
    notebook[heading].append(code)


def drop_note(notebook, heading, code):
    heading = heading.lower()
    if heading in notebook and code in notebook[heading]:
        notebook[heading].remove(code)


def fill_notes():
    store.code_notes.clear()
    store.city_notes.clear()
    store.status_notes.clear()
    for parcel in store.all_pages:
        code = parcel["tracking_code"]
        store.code_notes[code] = parcel
        add_note(store.city_notes, parcel["destination"], code)
        add_note(store.status_notes, parcel["status"], code)


def find_code(code):
    if code in store.code_notes:
        return store.code_notes[code]
    return None


def from_index(notebook, heading):
    heading = heading.strip().lower()
    if heading in notebook:
        return notebook[heading]
    return []


def city_list(city):
    return from_index(store.city_notes, city)


def status_list(status):
    return from_index(store.status_notes, status)
