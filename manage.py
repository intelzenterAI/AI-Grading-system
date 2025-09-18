"""
manage.py
---------
One-stop management script for IGCSE short-answer grader.
Now supports:
- Add questions
- Add student answers
- Add teacher labels
- Run grading (AI marks) -> CSV
- Run evaluation (AI vs Teacher) -> CSV
"""

import json
from pathlib import Path
import subprocess
import sys
import csv

ROOT = Path(__file__).parent
QFILE = ROOT / "model_answers.json"
SFILE = ROOT / "student_answers.json"
TFILE = ROOT / "teacher_labels.json"
GRADING_CSV = ROOT / "grading_results.csv"
EVAL_CSV = ROOT / "evaluation_results.csv"

def load_json(file, default):
    if file.exists():
        return json.loads(file.read_text(encoding="utf-8"))
    return default

def save_json(file, data):
    file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Updated {file.name}")

# ------------------- QUESTION -------------------
def add_question():
    data = load_json(QFILE, {})
    qid = input("Enter Question ID (e.g., q3): ").strip()
    if qid in data:
        print("⚠️ That question ID already exists.")
        return
    question = input("Enter question text: ").strip()
    max_marks = int(input("Enter maximum marks: ").strip())
    points = []
    print("\nEnter marking points (type 'done' to finish):")
    while True:
        pt = input(f" - Mark point {len(points)+1}: ").strip()
        if pt.lower() == "done":
            break
