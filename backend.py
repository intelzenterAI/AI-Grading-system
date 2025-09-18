from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import json
import uuid
import pytesseract
from PIL import Image
from main import grade_all, evaluate

ROOT = Path(__file__).parent
QFILE = ROOT / "model_answers.json"
SFILE = ROOT / "student_answers.json"
TFILE = ROOT / "teacher_labels.json"

app = FastAPI(title="IGCSE Short-Answer Grader API")

def load_json(file, default):
    if file.exists():
        return json.loads(file.read_text(encoding="utf-8"))
    return default

def save_json(file, data):
    file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

@app.post("/api/add_question")
async def add_question(qid: str = Form(...), question: str = Form(...), max_marks: int = Form(...), points: str = Form(...)):
    data = load_json(QFILE, {})
    if qid in data:
        return {"status": "error", "message": "Question ID already exists"}
    points_list = [p.strip() for p in points.split("\n") if p.strip()]
    data[qid] = {"question": question, "points": points_list, "max_marks": max_marks}
    save_json(QFILE, data)
    return {"status": "ok", "message": f"Question {qid} added"}

@app.post("/api/add_student")
async def add_student(id: str = Form(...), qid: str = Form(...), answer: str = Form(...)):
    data = load_json(SFILE, [])
    data.append({"id": id, "qid": qid, "answer": answer})
    save_json(SFILE, data)
    return {"status": "ok", "message": f"Student {id} answer added"}

@app.post("/api/add_teacher_label")
async def add_teacher_label(student_id: str = Form(...), qid: str = Form(...), teacher_mark: int = Form(...)):
    data = load_json(TFILE, [])
    data.append({"student_id": student_id, "qid": qid, "teacher_mark": teacher_mark})
    save_json(TFILE, data)
    return {"status": "ok", "message": f"Teacher mark added for {student_id}"}

@app.post("/api/upload_scans")
async def upload_scans(files: list[UploadFile] = File(...)):
    data = load_json(SFILE, [])
    uploaded, ocr_results = [], []
    for f in files:
        content = await f.read()
        temp_file = ROOT / f.filename
        with open(temp_file, "wb") as out:
            out.write(content)
        # OCR
        img = Image.open(temp_file)
        text = pytesseract.image_to_string(img)
        sid = "ocr_" + str(uuid.uuid4())[:8]
        qid = "unknown"  # teacher can later edit
        data.append({"id": sid, "qid": qid, "answer": text})
        uploaded.append({"filename": f.filename, "id": sid})
        ocr_results.append({"id": sid, "text": text})
    save_json(SFILE, data)
    return {"uploaded": uploaded, "ocr_results": ocr_results}

@app.get("/api/grade")
async def api_grade():
    results = grade_all(QFILE, SFILE)
    return JSONResponse(results)

@app.get("/api/evaluate")
async def api_evaluate():
    results = evaluate(QFILE, SFILE, TFILE)
    return JSONResponse(results)
