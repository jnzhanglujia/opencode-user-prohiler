#!/usr/bin/env python3
"""Safe JSON updater for user-data.json. Zero dependencies."""
import json, sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "user-data.json"

def main():
    if len(sys.argv) < 3:
        print("Usage: update_helper.py --path <dot.notation> --value '<json_or_string>'")
        sys.exit(1)

    path = sys.argv[sys.argv.index("--path") + 1]
    value = sys.argv[sys.argv.index("--value") + 1]

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        parsed = value

    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    keys = path.split(".")
    current = data
    for k in keys[:-1]:
        current = current.setdefault(k, {})
    current[keys[-1]] = parsed

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Updated '{path}' → {parsed}")

if __name__ == "__main__":
    main()
