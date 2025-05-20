import tensorflow as tf
from quickdraw import QuickDrawDataGroup
import numpy as np
from PIL import Image
from itertools import islice

# 1) 대상 동물 리스트
target_animals = ["cat", "dog", "elephant", "lion", "butterfly"]

# 2) quickdraw 패키지로 각 동물별 스케치 200장만 로드
num_samples = 200
images, labels = [], []
for idx, animal in enumerate(target_animals):
    print(f"loading {animal} sketches…")
    qdg = QuickDrawDataGroup(animal)
    # qdg.drawings는 generator → islice로 일부만 가져오기
    for drawing in islice(qdg.drawings, num_samples):
        # drawing.image: PIL.Image (256×256 RGB)
        img = drawing.image.convert("L").resize((28,28))
        arr = np.array(img, dtype=np.float32) / 255.0  # 0~1 정규화
        images.append(arr[..., None])                  # (28,28,1)
        labels.append(idx)
    print(f"{animal} load complete")

# 3) NumPy 배열로 변환
x = np.stack(images)    # shape = (len(target_animals)*num_samples, 28,28,1)
y = np.array(labels)    # shape = (len(target_animals)*num_samples,)

# 4) tf.data 파이프라인 구성 (80% train / 20% val)
batch_size = 128
AUTOTUNE = tf.data.AUTOTUNE

ds = tf.data.Dataset.from_tensor_slices((x, y))
ds = ds.shuffle(len(x))
train_size = int(len(x) * 0.8)
ds_train = ds.take(train_size).batch(batch_size).prefetch(AUTOTUNE)
ds_val   = ds.skip(train_size).batch(batch_size).prefetch(AUTOTUNE)

# 5) 모델 정의
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(28,28,1)),
    tf.keras.layers.Conv2D(32, 3, activation="relu"),
    tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(len(target_animals))
])
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer="adam",
    metrics=["accuracy"]
)

# 6) 학습
model.fit(ds_train, epochs=20, validation_data=ds_val)

# 7) 사용자 스케치 예측 함수
def predict_sketch(path):
    img = Image.open(path).convert("L").resize((28,28))
    arr = np.array(img, dtype=np.float32) / 255.0
    inp = arr[None,...,None]  # shape (1,28,28,1)
    logits = model(inp)
    idx = tf.argmax(logits, axis=1).numpy()[0]
    return target_animals[idx]

# 사용 예
print("Predict →", predict_sketch("public/my_sketch5_elephant.png"))
