import cv2
import os
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import roc_curve, auc

max_frames = 100  # Максимальное количество кадров для преобразования

def load_video(path):
    cap = cv2.VideoCapture(path)
    frames = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (128, 128))
        frames.append(frame)
    cap.release()
    return frames

model = load_model('model.h5')
# Путь к папке с видео
video_folder = 'real+deepfake'

# Списки для хранения истинных и предсказанных меток
true_labels = [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0]
predicted_labels = []

# Проход по всем файлам в папке
for file_name in os.listdir(video_folder):
    # Фильтрация только для видео файлов
    if file_name.endswith('.mp4') or file_name.endswith('.avi'):
        # Загрузка видео
        video_path = os.path.join(video_folder, file_name)
        video = cv2.VideoCapture(video_path)

        test_frames = load_video(video_path)  # Загрузка и предобработка кадров
        while len(test_frames) < max_frames:
            test_frames.append(np.zeros(test_frames[0].shape, dtype=np.uint8))
        test_frames = np.array(test_frames[:max_frames])  # Преобразование к массиву кадров

        prediction = model.predict(np.array([test_frames]))  # Предсказание
        if prediction[0] < 0.3:
            result = "Real Video"
            predicted_label = 0
        else:
            result = "Deepfake Video"
            predicted_label = 1
        predicted_labels.append(predicted_label)

        print("The video is:", result)

# Вычисление метрик
accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels)
recall = recall_score(true_labels, predicted_labels)
f1 = f1_score(true_labels, predicted_labels)
fpr, tpr, thresholds = roc_curve(true_labels, predicted_labels)
roc_auc = auc(fpr, tpr)

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")
print(f"AUC-ROC: {roc_auc:.2f}")
