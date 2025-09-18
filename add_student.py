"""
add_student.py
---------------
Helper script for teachers to add new student answers into student_answers.json
without editing JSON manually.
"""

import json
from pathlib import Path

FILE = Path(__file__).parent / "student_answers.json"

def load_student_answers():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8"))
    else:
        return []

def save_student_answers(data):
    FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Updated {FILE}")

def add_student_answer():
    data = load_student_answers()

    student_id = input("Enter Student ID (e.g., s5): ").strip()
    qid = input("Enter Question ID (must match one in model_answers.json, e.g., q1): ").strip()
    answer = input("Enter Student Answer: ").strip()

    # Append entry
    entry = {
        "id": student_id,
        "qid": qid,
        "answer": answer
    }
    data.append(entry)

    save_student_answers(data)
    print(f"✅ Student answer added successfully for {student_id}, question {qid}!")

if __name__ == "__main__":
    add_student_answer()
