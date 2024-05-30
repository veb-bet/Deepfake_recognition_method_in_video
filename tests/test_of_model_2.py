import cv2
import os
from tensorflow.keras.models import load_model
import numpy as np

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
video_folder = 'images'

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
        print(prediction[0])
        if prediction[0] < 0.3:
            result = "Real Video"
        else:
            result = "Deepfake Video"

        print("The video is:", result)