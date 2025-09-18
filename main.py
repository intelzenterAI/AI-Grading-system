"""
IGCSE Short-Answer Grader Prototype
-----------------------------------
Usage:
  python main.py grade                 # grades student answers and prints results
  python main.py evaluate              # runs a simple evaluation vs teacher labels

This prototype uses sentence-transformers embeddings (all-MiniLM-L6-v2) to compute
cosine similarity between student answers and model answer points. Each model point
represents a 1-mark "key point". Thresholds determine awarded marks.

IMPORTANT:
- This is a prototype. For production, collect labelled data to tune thresholds,
  add teacher-in-the-loop review, and sandbox any code execution (if grading code).
"""

import json
import sys
from pathlib import Path
import numpy as np

# The grading logic is separated so it can be unit tested.
def score_short_answer_similarity(student_answer, model_points, emb_model,
                                  thresholds=(0.85,0.75,0.6), max_marks=None):
    """
    emb_model: any object with an encode(list_of_texts) -> numpy array API (sentence-transformers-like)
    model_points: list of canonical answer points (strings)
    thresholds: similarity thresholds used for deciding matched points (tune these)
    max_marks: maximum marks for the question (by default len(model_points))
    returns: awarded_marks (int), details (dict)
    """
    if max_marks is None:
        max_marks = len(model_points)
    # encode
    emb_student = emb_model.encode([student_answer])
    emb_models = emb_model.encode(model_points)
    # normalize
    def norm(x):
        return x / np.linalg.norm(x, axis=1, keepdims=True)
    emb_student_n = norm(emb_student)
    emb_models_n = norm(emb_models)
    sims = (emb_student_n @ emb_models_n.T)[0]  # cosine similarities
    # Count points above lowest threshold (thresholds[-1])
    matched = sims >= thresholds[-1]
    points = int(matched.sum())
    awarded = min(max_marks, points)
    details = {"similarities": sims.tolist(),
               "matched_indices": [int(i) for i, m in enumerate(matched) if m]}
    return awarded, details

def load_json(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def grade_all(model_answers_path, student_answers_path, model_name='all-MiniLM-L6-v2'):
    from sentence_transformers import SentenceTransformer
    emb = SentenceTransformer(model_name)
    model_answers = load_json(model_answers_path)  # dict: qid -> { 'points': [...], 'max_marks': int }
    students = load_json(student_answers_path)     # list of submissions: { 'id': , 'qid': , 'answer': }
    results = []
    for s in students:
        qid = s['qid']
        m = model_answers[qid]
        awarded, details = score_short_answer_similarity(
            s['answer'], m['points'], emb, max_marks=m.get('max_marks'))
        results.append({
            "student_id": s['id'],
            "qid": qid,
            "answer": s['answer'],
            "awarded": awarded,
            "max_marks": m.get('max_marks'),
            "details": details
        })
    print(json.dumps(results, indent=2, ensure_ascii=False))

def evaluate(model_answers_path, student_answers_path, teacher_labels_path,
             model_name='all-MiniLM-L6-v2'):
    from sentence_transformers import SentenceTransformer
    emb = SentenceTransformer(model_name)
    model_answers = load_json(model_answers_path)
    students = load_json(student_answers_path)
    teacher = load_json(teacher_labels_path)  # list of { student_id, qid, teacher_mark }
    # build map for quick lookup
    teacher_map = {(t['student_id'], t['qid']): t['teacher_mark'] for t in teacher}
    total = 0
    correct = 0
    diffs = []
    for s in students:
        key = (s['id'], s['qid'])
        awarded, details = score_short_answer_similarity(
            s['answer'], model_answers[s['qid']]['points'], emb,
            max_marks=model_answers[s['qid']].get('max_marks'))
        teacher_mark = teacher_map.get(key)
        if teacher_mark is None:
            continue
        total += 1
        correct += 1 if awarded == teacher_mark else 0
        diffs.append({"student_id": s['id'], "qid": s['qid'],
                      "awarded": awarded, "teacher": teacher_mark})
    acc = correct / total if total else None
    print("Evaluation Results")
    print("==================")
    print(f"Total compared: {total}")
    print(f"Exact match accuracy: {acc:.3f}" if acc is not None else "No matching teacher labels found")
    print("Differences (sample):")
    print(json.dumps(diffs[:20], indent=2, ensure_ascii=False))

if __name__ == '__main__':
    root = Path(__file__).parent
    model_answers_path = root / "model_answers.json"
    student_answers_path = root / "student_answers.json"
    teacher_labels_path = root / "teacher_labels.json"
    if len(sys.argv) < 2:
        print("Usage: python main.py [grade|evaluate]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'grade':
        grade_all(model_answers_path, student_answers_path)
    elif cmd == 'evaluate':
        evaluate(model_answers_path, student_answers_path, teacher_labels_path)
    else:
        print("Unknown command")
