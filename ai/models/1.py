import tensorflow as tf

# 1) 기존 HDF5 모델 로드 (compile=False)
model_h5 = tf.keras.models.load_model(
    "ai/models/doodleNet-model.h5",
    compile=False
)

# 2) SavedModel 포맷으로 저장
model_h5.save(
    "ai/models/doodleNet_savedmodel",
    save_format="tf"  # TensorFlow SavedModel
)

print("SavedModel 형식으로 변환 완료: ai/models/doodleNet_savedmodel")
