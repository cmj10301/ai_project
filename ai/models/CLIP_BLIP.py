# 1) 필요한 도구 불러오기
import wikipedia
from transformers import CLIPProcessor, CLIPModel
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
from torch.nn import functional as F

# ─────────────────────────────────────────────────────
# 0) 위키백과 요약 함수
# ─────────────────────────────────────────────────────
def get_wiki_summary(term, sentences=2):
    wikipedia.set_lang("ko")  # 한국어 위키백과 사용
    try:
        return wikipedia.summary(term, sentences=sentences)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"여러 항목({e.options[:3]})이 있어요. 더 구체적인 이름을 입력해 주세요."
    except wikipedia.exceptions.PageError:
        return "위키백과에 해당 페이지가 없어요."


# 2) 이미지 열기
img = Image.open("public/test_img2.png").convert("RGB")

# ─────────────────────────────────────────────────────
# A) CLIP: 미리 정해둔 후보 리스트에서 이 이미지가 무엇인지 분류
# ─────────────────────────────────────────────────────
# 2-1) CLIP 모델·전처리 준비
clip_model     = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# 2-2) 우리가 맞추고 싶은 물건(예: 동물, 제품 이름) 후보 리스트
candidates = ["cat", "dog", "bicycle", "car", "flower"]

# 2-3) CLIP 전처리: 이미지와 텍스트를 숫자로 바꿔 줌
inputs = clip_processor(text=candidates, images=img, return_tensors="pt", padding=True)

# 2-4) CLIP 임베딩 얻기
outputs      = clip_model(**inputs)
img_emb      = outputs.image_embeds        # 이미지 벡터
txt_emb      = outputs.text_embeds         # 텍스트 벡터

# 2-5) 코사인 유사도로 가장 비슷한 후보 찾기
sims         = F.cosine_similarity(
                   img_emb.unsqueeze(1),
                   txt_emb.unsqueeze(0),
                   dim=-1
               )
probs        = sims.softmax(dim=1)[0]      # 0번째 이미지 확률
best_index   = torch.argmax(probs).item()
label = candidates[best_index]

print("CLIP 분류 결과:", label, f"(확률 {probs[best_index]:.2f})")


# ─────────────────────────────────────────────────────
# B) BLIP: 이미지 캡션(무엇이 있는지 설명) 생성
# ─────────────────────────────────────────────────────
# 2-6) BLIP 모델·전처리 준비
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model     = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# 2-7) BLIP 전처리
blip_inputs = blip_processor(images=img, return_tensors="pt")

# 2-8) 캡션 생성
out           = blip_model.generate(**blip_inputs)
caption       = blip_processor.decode(out[0], skip_special_tokens=True)

print(f"BLIP 이미지 설명: {caption}")

# ─────────────────────────────────────────────────────
# C) 분류된 대상의 추가 정보: 위키백과 요약
# ─────────────────────────────────────────────────────
# 영어 이름을 한글로 바꿀 사전
eng2kor = {
    "cat": "고양이",
    "dog": "개",
    "bicycle": "자전거",
    "car": "자동차",
    "flower": "꽃"
}
kor_label = eng2kor.get(label, label)

print(f"\n=== {kor_label} 위키백과 요약 ===")
print(get_wiki_summary(kor_label, sentences=2))
