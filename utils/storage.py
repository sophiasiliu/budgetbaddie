# utils/storage.py

import json
from models.envelopes import Envelope

FILE = "envelopes.json"

def save_envelopes(envelopes):
    data = [env.__dict__ for env in envelopes]
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_envelopes():
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
            return [Envelope(**env) for env in data]
    except FileNotFoundError:
        return []
