import json
import os
from config import Config

def load_preferences():
    if os.path.exists(Config.PREFS_FILE):
        with open(Config.PREFS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_preference(key, val):
    prefs = load_preferences()
    prefs[key] = val
    with open(Config.PREFS_FILE, "w") as f:
        json.dump(prefs, f, indent=2)

def extract_preferences_from_msg(msg):
    body = msg.get("body", "")
    if "CC'd on anything that comes in from our lawyers at Hartwell & Cho" in body:
        save_preference("legal_cc", "priya@paperjet.io")
        return "Saved preference: CC priya@paperjet.io on Legal emails."
    if "I do not take meetings before 11:00am" in body:
        save_preference("no_early_meetings", True)
        return "Saved preference: No meetings before 11:00 AM."
    return None
