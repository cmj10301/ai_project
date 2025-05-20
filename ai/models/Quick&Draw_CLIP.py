from quickdraw import QuickDrawDataGroup
import numpy as np
import tensorflow as tf
from PIL import Image
from itertools import islice

# 1) 우리가 원하는 동물 리스트
target_animals = ["cat", "dog", "elephant", "lion", "butterfly"]

# 2) QuickDrawDataGroup 으로 각 동물 200장만 로드
images, labels = [], []
for idx, animal in enumerate(target_animals):
    qdg = QuickDrawDataGroup(animal)
    # qdg.drawings 는 무한 generator → islice 로 200개만 가져오기
    for drawing in islice(qdg.drawings, 200):
        # drawing.image 를 28×28 흑백으로 변환
        img = drawing.image.convert("L").resize((28,28))
        arr = np.array(img, np.float32) / 255.0
        images.append(arr[..., None])
        labels.append(idx)
        
# 3) NumPy 배열로 변환
x = np.array(images, dtype=np.float32)
y = np.array(labels, dtype=np.int32)

# 4) tf.data 파이프라인 구성
batch_size = 128
AUTOTUNE = tf.data.AUTOTUNE

ds_full = tf.data.Dataset.from_tensor_slices((x, y))
# 훈련/검증 분리 (80% train / 20% val)
train_size = int(len(x) * 0.8)
ds_train = ds_full.take(train_size)
ds_val   = ds_full.skip(train_size)

# 전처리: 섞고 배치, 프리페치
ds_train = (
    ds_train
    .shuffle(1000)
    .batch(batch_size)
    .prefetch(AUTOTUNE)
)
ds_val = (
    ds_val
    .batch(batch_size)
    .prefetch(AUTOTUNE)
)

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
model.fit(ds_train, epochs=10, validation_data=ds_val)

# 7) 사용자 스케치 예측 함수
from PIL import Image as PILImage

def predict_sketch(path):
    img = PILImage.open(path).convert("L").resize((28,28))
    arr = np.array(img, dtype=np.float32) / 255.0
    inp = arr[None,...,None]
    logits = model(inp)
    idx = tf.argmax(logits, axis=1).numpy()[0]
    return target_animals[idx]

# 사용 예
print(predict_sketch("public/my_sketch.png"))
