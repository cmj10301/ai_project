from transformers import CLIPProcessor, CLIPModel

# ① CLIP 모델과 전처리 도구 불러오기
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("모델과 전처리 도구가 준비되었습니다!")

from PIL import Image
import torch
from torch.nn import functional as F

# 1) 분석할 그림 불러오기
image = Image.open("public/test_img3.jpg")  

# 2) 맞추고 싶은 단어(동물) 목록 작성
texts = ["cat", "dog", "elephant", "lion", "butterfly", "redpanda"]

# 3) 전처리: 그림과 단어를 모델이 이해할 수 있게 숫자 형태로 바꿔줍니다.
inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)

# 이제 inputs에는 아래 두 가지 정보가 들어 있어요.
# - inputs["pixel_values"]: 그림을 숫자(픽셀 값)로 바꾼 텐서
# - inputs["input_ids"], inputs["attention_mask"]: 단어를 숫자(토큰)로 바꾼 텐서

# 4) (이 단계에서 바로 예측까지 할 수도 있지만, 먼저 전처리 결과 모양을 확인해 볼게요)
print("그림 전처리 결과 크기:", inputs["pixel_values"].shape)
print("단어 전처리 결과 크기:", inputs["input_ids"].shape)

# ① 모델에 전처리된 inputs를 넣어 임베딩(숫자 벡터) 얻기
outputs = model(**inputs)
image_embeds = outputs.image_embeds    # 그림 임베딩 벡터
text_embeds  = outputs.text_embeds     # 단어 임베딩 벡터

# image_embeds: [배치 크기, 임베딩 차원]
# text_embeds:  [단어 갯수, 임베딩 차원]
# 아래 코드는 각 그림과 각 단어의 유사도를 하나의 행렬로 계산해요.
logits_per_image = F.cosine_similarity(
    image_embeds.unsqueeze(1),  # 그림 벡터 차원을 맞추기 위해 1번 축에 차원 추가
    text_embeds.unsqueeze(0),   # 단어 벡터 차원을 맞추기 위해 0번 축에 차원 추가
    dim=-1
)

# ③ 확률로 바꿔서 가장 높은 단어 찾기
probs = logits_per_image.softmax(dim=1)  
best_index = probs.argmax(dim=1).item()  # 확률이 가장 높은 단어의 인덱스

# ④ 결과 출력
print("예측 동물:", texts[best_index])
print("확률:", probs[0, best_index].item())
