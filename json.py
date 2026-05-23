import os
import json
def load_high_score():
    if os.path.exists(RECORD_FILE):
        try:
            with open(RECORD_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except (json.JSONDecodeError, KeyError):
            return 0
    return 0

def save_high_score(score):
    with open(RECORD_FILE, "w") as f:
        json.dump({"high_score": score}, f)