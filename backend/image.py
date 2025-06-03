from fastapi import APIRouter, Request
from pydantic import BaseModel
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import base64
import io
import requests

router = APIRouter()

# 모델 및 프로세서 로딩 (최초 1회)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

class ImageRequest(BaseModel):
    image: str  # base64 string

@router.post("/api/image")
async def analyze_image(req: ImageRequest):
    # base64 디코딩
    header, encoded = req.image.split(",", 1)
    image = Image.open(io.BytesIO(base64.b64decode(encoded))).convert("RGB")

    # 캡션 추출
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=20)
    caption = processor.decode(out[0], skip_special_tokens=True)

    # 위키백과 검색
    query = caption.split(',')[0].strip().split(' ')[-1]  # 예시: 마지막 명사 추출
    summary = fetch_wikipedia_summary(query)

    return {"caption": caption, "keyword": query, "summary": summary}

def fetch_wikipedia_summary(query: str) -> str:
    url = f"https://ko.wikipedia.org/api/rest_v1/page/summary/{query}"
    resp = requests.get(url)
    if resp.status_code == 200 and 'extract' in resp.json():
        return resp.json()['extract']
    else:
        return "📌 위키백과에서 정보를 찾을 수 없습니다."
