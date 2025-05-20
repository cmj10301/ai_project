import tensorflow as tf
import numpy as np
from quickdraw import QuickDrawDataGroup
from itertools import islice
from PIL import Image

# 0) SavedModel 로드
model = tf.keras.models.load_model("ai/models/doodleNet_savedmodel")

# 1) class_names.txt에서 클래스 이름 리스트 로드
#    파일에 1개 클래스 이름이 1라인씩 저장되어 있다고 가정합니다.
with open("ai/models/class_names.txt", encoding="utf-8") as f:
    class_names = [line.strip() for line in f if line.strip()]

# 2) 테스트할 소수 클래스 & 해당 인덱스 구하기
target_animals = ["cat", "dog", "elephant", "lion", "butterfly"]
target_indices = [class_names.index(a) for a in target_animals]

# 3) 평가 함수
def evaluate_model(model, target_animals, target_indices, num_samples=200):
    correct = total = 0
    for animal, idx in zip(target_animals, target_indices):
        print(f"Evaluating {animal}...")
        qdg = QuickDrawDataGroup(animal)
        for drawing in islice(qdg.drawings, num_samples):
            img = drawing.image.convert("L").resize((28,28))
            inp = np.array(img, np.float32)[None,...,None] / 255.0
            pred = np.argmax(model.predict(inp), axis=1)[0]
            total += 1
            if pred == idx:
                correct += 1
    print(f"Accuracy on {target_animals}: {correct/total:.2%}")

# 4) 스케치 예측 함수
def predict_sketch(model, path):
    img = Image.open(path).convert("L").resize((28,28))
    inp = np.array(img, np.float32)[None,...,None] / 255.0
    pred = np.argmax(model.predict(inp), axis=1)[0]
    return class_names[pred]

if __name__ == "__main__":
    evaluate_model(model, target_animals, target_indices)
    print("Predict →", predict_sketch(model, "public/my_sketch.png"))
