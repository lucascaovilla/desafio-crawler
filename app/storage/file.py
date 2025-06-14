import json
import csv
from pathlib import Path

def save_as_json(data, filename):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved JSON to {filename}")

def save_as_csv(data, filename):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved CSV to {filename}")
