IGCSE Short-Answer Grader Prototype
==================================

This prototype grades short/structured answers by comparing student answers to model "mark points"
using sentence-transformers embeddings and cosine similarity.

Files:
- main.py               : CLI to grade and evaluate
- model_answers.json    : Model answers and marking points (qid -> points)
- student_answers.json  : Example student submissions
- teacher_labels.json   : Example teacher-assigned marks for evaluation
- requirements.txt      : Python dependencies

Usage (local machine):
1. Create and activate a Python virtual environment:
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run grading:
   python main.py grade

4. Run evaluation (requires teacher_labels.json):
   python main.py evaluate

Notes:
- Tuning thresholds in main.py is essential for good performance.
- Collect labelled training data (student answers with teacher marks) to tune or fine-tune a model.
- For production, add teacher-in-the-loop, UI, and better explainability features.
