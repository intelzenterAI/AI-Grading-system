# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

# Allow all origins (for Colab frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def read_root():
    return {"message": "Backend is running successfully!"}

@app.post("/api/add_question")
async def add_question(request: Request):
    data = await request.json()
    file_path = os.path.join(BASE_DIR, "model_answers.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            questions = json.load(f)
    else:
        questions = []

    questions.append(data)
    with open(file_path, "w") as f:
        json.dump(questions, f, indent=2)

    return JSONResponse(content={"status": "success", "message": "Question added successfully"})
