"""
add_teacher_label.py
--------------------
Helper script for teachers to add teacher-marked scores into teacher_labels.json
without editing JSON manually.
"""

import json
from pathlib import Path

FILE = Path(__file__).parent / "teacher_labels.json"

def load_teacher_labels():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8"))
    else:
        return []

def save_teacher_labels(data):
    FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Updated {FILE}")

def add_teacher_label():
    data = load_teacher_labels()

    student_id = input("Enter Student ID (e.g., s1): ").strip()
    qid = input("Enter Question ID (e.g., q1): ").strip()
    mark = int(input("Enter Teacher Mark (integer): ").strip())

    entry = {
        "student_id": student_id,
        "qid": qid,
        "teacher_mark": mark
    }

    data.append(entry)
    save_teacher_labels(data)
    print(f"✅ Teacher mark recorded for {student_id}, {qid}: {mark}")

if __name__ == "__main__":
    add_teacher_label()
