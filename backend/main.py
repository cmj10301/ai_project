from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.ai.sketch_predict import predict_sketch
from pydantic import BaseModel
from datetime import datetime
from backend.mongoDBConnect import feedback_collection

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# CORS 허용 (프론트와 통신)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 모델
class SketchRequest(BaseModel):
    image: str  # base64 PNG

@app.post("/api/sketch")
async def sketch_api(req: SketchRequest):
    prediction = predict_sketch(req.image)
    return {"prediction": prediction}

class FeedbackRequest(BaseModel):
    image: str  # base64
    prediction: str
    is_correct: bool
    correct_label: str | None = None  # 사용자가 직접 정답을 입력한 경우 (선택)

@app.post("/api/feedback")
async def feedback_api(req: FeedbackRequest):
    print(f"✅ inserting feedback: {req.prediction} / is_correct: {req.is_correct}")
    doc = {
        "image_base64": req.image,
        "predicted": req.prediction,
        "is_correct": req.is_correct,
        "correct_label": req.correct_label,
        "timestamp": datetime.utcnow()
    }
    feedback_collection.insert_one(doc)
    return {"message": "Feedback saved"}