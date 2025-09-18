"""
add_question.py
---------------
Helper script for teachers to add new IGCSE-style short-answer questions and mark schemes
to model_answers.json without editing JSON manually.
"""

import json
from pathlib import Path

FILE = Path(__file__).parent / "model_answers.json"

def load_model_answers():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8"))
    else:
        return {}

def save_model_answers(data):
    FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Updated {FILE}")

def add_question():
    data = load_model_answers()
    qid = input("Enter Question ID (e.g., q3): ").strip()
    if qid in data:
        print("⚠️ That question ID already exists. Use a unique ID.")
        return

    question = input("Enter question text: ").strip()
    max_marks = int(input("Enter maximum marks: ").strip())
    
    print("\nNow enter the marking points (type 'done' when finished):")
    points = []
    while True:
        pt = input(f" - Mark point {len(points)+1}: ").strip()
        if pt.lower() == "done":
            break
        if pt:
            points.append(pt)

    data[qid] = {
        "question": question,
        "points": points,
        "max_marks": max_marks
    }

    save_model_answers(data)
    print(f"✅ Question {qid} added successfully!")

if __name__ == "__main__":
    add_question()
