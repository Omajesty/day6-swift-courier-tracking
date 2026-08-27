import os

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
book_file = os.path.join(base_path, "parcels.json")
seal_file = os.path.join(base_path, "ledger.seal")
staff_file = os.path.join(base_path, "staff.json")

all_pages = []
code_notes = {}
city_notes = {}
status_notes = {}
ask_count = {}
seal_broken = False
