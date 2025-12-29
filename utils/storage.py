# utils/storage.py

import json
import os
from models.envelopes import Envelope

ENVELOPES_FILE = "envelopes.json"
SETTINGS_FILE = "settings.json"


# -------------------- ENVELOPES --------------------

def save_envelopes(envelopes):
    """Save all envelope objects to JSON."""
    data = [env.__dict__ for env in envelopes]
    with open(ENVELOPES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_envelopes():
    """Load envelopes from JSON, return list of Envelope objects."""
    try:
        with open(ENVELOPES_FILE, "r") as f:
            data = json.load(f)
            return [Envelope(**env) for env in data]
    except FileNotFoundError:
        return []


# -------------------- SETTINGS (money_to_budget) --------------------

def load_settings():
    """Return settings dict — at minimum money_to_budget."""
    if not os.path.exists(SETTINGS_FILE):
        return {"money_to_budget": 0.00}

    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # corrupted settings file safety fallback
        return {"money_to_budget": 0.00}


def save_settings(money_to_budget):
    """Save money_to_budget to the settings file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"money_to_budget": money_to_budget}, f, indent=2)

