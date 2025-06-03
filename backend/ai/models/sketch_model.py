import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping

# 1. 클래스 이름 불러오기
def get_classes_from_folder(data_dir):
    return sorted([
        filename.replace('.npy', '')
        for filename in os.listdir(data_dir)
        if filename.endswith('.npy')
    ])

# 2. 데이터 로딩
def load_quickdraw_dataset(data_dir, class_names, samples_per_class=2000):
    X = []
    y = []
    for class_name in class_names:
        path = os.path.join(data_dir, class_name + '.npy')
        drawings = np.load(path, mmap_mode='r')
        drawings = drawings[:samples_per_class]
        drawings = drawings / 255.0
        drawings = drawings.reshape(-1, 28, 28, 1)
        X.append(drawings)
        y.extend([class_name] * len(drawings))
    X = np.concatenate(X, axis=0)
    return X, y

# 3. 모델 정의
def create_model_mobilenetv2(num_classes):
    base_model = MobileNetV2(
        input_shape=(96, 96, 3),
        include_top=False,
        weights=None,
        pooling='avg'
    )
    model = models.Sequential([
        layers.Input(shape=(28, 28, 1)),
        layers.Resizing(96, 96),                   # 입력 크기 확대
        layers.Conv2D(3, 1, padding='same'),       # 흑백 → 3채널 RGB로 흉내
        base_model,
        layers.Dense(256, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

# 4. 학습 함수
def train():
    data_dir = 'backend/ai/dataset/numpy_bitmap'
    output_model_path = 'backend/ai/outputs/sketch_model.keras'
    class_list_path = 'backend/ai/outputs/classes.txt'

    class_names = get_classes_from_folder(data_dir)
    print("✅ 클래스 수:", len(class_names))

    X, y_text = load_quickdraw_dataset(data_dir, class_names, samples_per_class=2000)

    encoder = LabelEncoder()
    y_int = encoder.fit_transform(y_text)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y_int, test_size=0.1, random_state=42, stratify=y_int
    )

    y_train_cat = tf.keras.utils.to_categorical(y_train, num_classes=len(class_names))
    y_val_cat = tf.keras.utils.to_categorical(y_val, num_classes=len(class_names))

    model = create_model_mobilenetv2(num_classes=len(class_names))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # ✅ 클래스 불균형 보정
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(y_int),
        y=y_int
    )
    class_weight_dict = {i: w for i, w in enumerate(class_weights)}

    early_stop = EarlyStopping(patience=3, restore_best_weights=True)

    model.fit(
        X_train, y_train_cat,
        batch_size=64,
        epochs=5,
        validation_data=(X_val, y_val_cat),
        callbacks=[early_stop],
        class_weight=class_weight_dict
    )

    model.save(output_model_path)
    print(f"✅ 모델 저장됨: {output_model_path}")

    with open(class_list_path, 'w', encoding='utf-8') as f:
        for name in class_names:
            f.write(name + '\n')
    print(f"✅ 클래스 목록 저장됨: {class_list_path}")

if __name__ == "__main__":
    train()
