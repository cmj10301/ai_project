from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # 반드시 있어야 함

MONGO_URI = os.environ.get("MONGODB_URI")
if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI 환경변수가 설정되지 않았습니다.")

client = MongoClient(MONGO_URI)
db = client["ai_service"]  # Atlas에서 만든 DB명
feedback_collection = db["user_feedback"]
