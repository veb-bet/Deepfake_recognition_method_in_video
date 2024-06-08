from tensorflow.keras.models import load_model
import cv2
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Загрузка предобученной модели
model = load_model('deepfake_detection_model.h5')

# Загрузка тестового видео
test_video = cv2.VideoCapture('id0_id2_0004.mp4')

# Предобработка кадров видео
frames = []
while True:
    ret, frame = test_video.read()
    if not ret:
        break
    frame = cv2.resize(frame, (224, 224))
    frames.append(frame)

X_test = np.array(frames)
X_test = X_test.reshape((-1,) + (224, 224, 3))

# Предсказание модели
y_pred = model.predict(X_test)

# Определение класса
class_labels = ['Deepfake', 'Real']
y_pred_class = [class_labels[int(np.round(y))] for y in y_pred]

# Вывод результата
for i, pred in enumerate(y_pred_class):
    print(f"Frame {i}: {pred}")

# Расчет метрик
y_true = ['Deepfake' if i < len(frames)//2 else 'Real' for i in range(len(frames))]
accuracy = accuracy_score(y_true, y_pred_class)
precision = precision_score(y_true, y_pred_class, pos_label='Deepfake')
recall = recall_score(y_true, y_pred_class, pos_label='Deepfake')
f1 = f1_score(y_true, y_pred_class, pos_label='Deepfake')

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")
