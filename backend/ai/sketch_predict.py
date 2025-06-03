import io
import base64
import numpy as np
from PIL import Image
import tensorflow as tf

# 모델 및 클래스 로딩
model = tf.keras.models.load_model('backend/ai/outputs/sketch_model.keras')
with open('backend/ai/outputs/classes.txt', 'r', encoding='utf-8') as f:
    class_names = [line.strip() for line in f]

def predict_sketch(base64_image: str) -> str:
    header, encoded = base64_image.split(',', 1)
    image_bytes = base64.b64decode(encoded)

    img = Image.open(io.BytesIO(image_bytes)).convert('L').resize((28, 28))
    img_np = np.array(img).astype(np.float32) / 255.0
    img_np = img_np.reshape(1, 28, 28, 1)

    # ✅ MobileNetV2 입력 규격에 맞게 전처리
    img_tf = tf.image.resize(img_np, [96, 96])
    img_tf = tf.image.grayscale_to_rgb(img_tf)

    preds = model.predict(img_tf)
    

    print("🔍 raw prediction:", preds)  # 확률 벡터 출력
    print("🔍 predicted index:", np.argmax(preds))
    print("🔍 predicted class:", class_names[np.argmax(preds)])
    print("🔍 top 5 predictions:", sorted(
        [(class_names[i], float(prob)) for i, prob in enumerate(preds[0])],
        key=lambda x: x[1], reverse=True
    )[:5])

    predicted_index = np.argmax(preds)
    return class_names[predicted_index]
