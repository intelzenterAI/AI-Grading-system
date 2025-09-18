"""
manage.py
---------
One-stop management script for IGCSE short-answer grader.
Allows teachers to add questions, student answers, and teacher labels
from a single menu-driven interface.
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent
QFILE = ROOT / "model_answers.json"
SFILE = ROOT / "student_answers.json"
TFILE = ROOT / "teacher_labels.json"

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
        if pt:
            points.append(pt)
    data[qid] = {"question": question, "points": points, "max_marks": max_marks}
    save_json(QFILE, data)
    print(f"✅ Question {qid} added.\n")

# ------------------- STUDENT -------------------
def add_student_answer():
    data = load_json(SFILE, [])
    sid = input("Enter Student ID (e.g., s5): ").strip()
    qid = input("Enter Question ID (e.g., q1): ").strip()
    answer = input("Enter Student Answer: ").strip()
    data.append({"id": sid, "qid": qid, "answer": answer})
    save_json(SFILE, data)
    print(f"✅ Answer added for {sid}, {qid}.\n")

# ------------------- TEACHER -------------------
def add_teacher_label():
    data = load_json(TFILE, [])
    sid = input("Enter Student ID (e.g., s1): ").strip()
    qid = input("Enter Question ID (e.g., q1): ").strip()
    mark = int(input("Enter Teacher Mark (integer): ").strip())
    data.append({"student_id": sid, "qid": qid, "teacher_mark": mark})
    save_json(TFILE, data)
    print(f"✅ Teacher mark recorded for {sid}, {qid}: {mark}\n")

# ------------------- MENU -------------------
def main():
    while True:
        print("\n=== IGCSE Short-Answer Grader Management ===")
        print("1. Add Question")
        print("2. Add Student Answer")
        print("3. Add Teacher Label")
        print("4. Exit")
        choice = input("Choose an option [1-4]: ").strip()
        if choice == "1":
            add_question()
        elif choice == "2":
            add_student_answer()
        elif choice == "3":
            add_teacher_label()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
