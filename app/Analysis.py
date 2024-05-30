from keras.models import load_model
import cv2
import numpy as np
from datetime import datetime


class Analysis:
    def __init__(self):
        self.model_path = 'model.h5'
        self.temp_path = 'temp/analyzed_video.mp4'
        self.video = None
        self.request_time = None
        self.is_fake = None
        self.fake_coefficient = None

    def clear_result(self):
        self.video = None
        self.request_time = None
        self.is_fake = None
        self.fake_coefficient = None

    def analyze(self):
        if self.video:
            self.request_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            model = load_model(self.model_path)
            with open(self.temp_path, 'wb') as file:
                file.write(self.video)

            cap = cv2.VideoCapture(self.temp_path)
            frames = []
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                # # wow this shit here shows pictures, prolly coud'ha make somee movieee watchiee from it
                # cv2.imshow('frame', frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
                frame = cv2.resize(frame, (128, 128))
                frames.append(frame)
            cap.release()

            max_frames = 100
            while len(frames) < max_frames:
                frames.append(np.zeros(frames[0].shape, dtype=np.uint8))
            frames = np.array(frames[:max_frames])  # Преобразование из List в numpy массив
            prediction = model.predict(np.array([frames]))[0][0]  # Предсказание

            # print("prediction: ", prediction)
            self.is_fake = prediction > 0.3
            self.fake_coefficient = prediction
            # print(prediction[0])
            # if prediction[0] < 0.3:
            #     result = "Real Video"
            # else:
            #     result = "Deepfake Video"
            # print("The video is:", result)
        else:
            return None
