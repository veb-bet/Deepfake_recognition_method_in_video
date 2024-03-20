import sys

import cv2
from tensorflow.keras.models import load_model
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, \
    QFileDialog, QLineEdit, QHBoxLayout, QMessageBox, QInputDialog, QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QPixmap


def load_video(path):
    cap = cv2.VideoCapture(path)
    frames = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (128, 128))
        frames.append(frame)
    cap.release()
    return frames

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Analyzer")
        self.setGeometry(50, 50, 600, 600)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.profile_tab = QWidget()
        self.history_tab = QWidget()
        self.analyze_tab = QWidget()

        self.tabs.addTab(self.profile_tab, "Профиль")
        self.tabs.addTab(self.history_tab, "История")
        self.tabs.addTab(self.analyze_tab, "Анализ")

        self.setup_profile_tab()
        self.setup_history_tab()
        self.setup_analyze_tab()

    def setup_profile_tab(self):
        layout = QVBoxLayout()

        avatar_layout = QHBoxLayout()  # Горизонтальный интерфейс для аватарки и кнопки
        self.avatar_image = QLabel()
        pixmap = QPixmap("avatar.png").scaled(100, 100)
        self.avatar_image.setPixmap(pixmap)
        self.avatar_image.setContentsMargins(15, 0, 0, 0)
        avatar_layout.addWidget(self.avatar_image)

        change_avatar_button = QPushButton("Сменить иконку профиля")
        avatar_layout.addWidget(change_avatar_button)

        layout.addLayout(
            avatar_layout)  # Добавляем горизонтальный интерфейс с аватаркой и кнопкой в вертикальный интерфейс

        user_layout = QHBoxLayout()
        self.username_text = QLabel("User_Ivanov22")
        self.username_text.setContentsMargins(15, 0, 0, 0)
        font = self.username_text.font()
        font.setBold(True)
        self.username_text.setFont(font)
        user_layout.addWidget(self.username_text)

        change_username_button = QPushButton("Сменить имя пользователя")
        user_layout.addWidget(change_username_button)
        layout.addLayout(
            user_layout)

        change_password_button = QPushButton("Изменить пароль")
        layout.addWidget(change_password_button)

        delete_account_button = QPushButton("Удалить аккаунт")
        layout.addWidget(delete_account_button)

        logout_button = QPushButton("Выйти из приложения")
        layout.addWidget(logout_button)

        self.profile_tab.setLayout(layout)

        change_avatar_button.clicked.connect(self.change_avatar)
        change_username_button.clicked.connect(self.change_username)
        change_password_button.clicked.connect(self.change_password)
        delete_account_button.clicked.connect(self.delete_account)
        logout_button.clicked.connect(self.logout)

    def change_username(self):
        new_username, ok = QInputDialog.getText(self, "Сменить имя пользователя", "Введите новое имя пользователя:")
        if ok and new_username:
            self.username_text.setText(new_username)

    def change_avatar(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите картинку", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            new_avatar = QPixmap(file_path).scaled(100, 100)
            self.avatar_image.setPixmap(new_avatar)

    def setup_history_tab(self):
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setRowCount(5)  # Установите количество строк
        table.setColumnCount(4)  # Установите количество столбцов

        table.setHorizontalHeaderLabels(["Дата анализа", "Результат", "Файл с видео", "Фидбек"])

        table.setItem(0, 0, QTableWidgetItem("01.01.2022"))
        table.setItem(0, 1, QTableWidgetItem("Дипфейк"))
        table.setItem(0, 2, QTableWidgetItem("video1.mp4"))
        table.setItem(0, 3, QTableWidgetItem("Спасибо"))

        table.setItem(1, 0, QTableWidgetItem("02.01.2022"))
        table.setItem(1, 1, QTableWidgetItem("Настоящее видео"))
        table.setItem(1, 2, QTableWidgetItem("video2.mp4"))
        table.setItem(1, 3, QTableWidgetItem("-"))

        table.setItem(2, 0, QTableWidgetItem("03.01.2022"))
        table.setItem(2, 1, QTableWidgetItem("Дипфейк"))
        table.setItem(2, 2, QTableWidgetItem("video3.mp4"))
        table.setItem(2, 3, QTableWidgetItem("-"))

        # Добавление таблицы в макет
        layout.addWidget(table)

        self.history_tab.setLayout(layout)

    def setup_analyze_tab(self):
        layout = QVBoxLayout()

        self.video_line_edit = QLineEdit()
        layout.addWidget(self.video_line_edit)

        self.upload_button = QPushButton("Загрузить видео")
        self.upload_button.clicked.connect(self.upload_video)
        layout.addWidget(self.upload_button)

        self.analyze_button = QPushButton("Анализировать")
        self.analyze_button.clicked.connect(self.analyze_video)
        layout.addWidget(self.analyze_button)

        self.analyze_tab.setLayout(layout)

    def change_password(self):
        # Обработчик нажатия кнопки "Изменить пароль"
        print("Пароль будет изменен")

    def delete_account(self):
        # Обработчик нажатия кнопки "Удалить аккаунт"
        message_box = QMessageBox()
        message_box.setWindowTitle("Подтверждение удаления аккаунта")
        message_box.setText("Вы уверены, что хотите удалить аккаунт?")
        message_box.setIcon(QMessageBox.Warning)
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)

        reply = message_box.exec()

        if reply == QMessageBox.Yes:
            print("Аккаунт удален")

    def logout(self):
        # Обработчик нажатия кнопки "Выйти из приложения"
        print("Выход из приложения")
        sys.exit()

    def upload_video(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите видео", "", "Video Files (*.mp4 *.avi)")
        self.video_line_edit.setText(file_path)

    def analyze_video(self):
        video_path = self.video_line_edit.text()
        self.model = load_model("model.h5")
        max_frames = 100
        test_frames = load_video(video_path)  # Загрузка и предобработка кадров
        while len(test_frames) < max_frames:
            test_frames.append(np.zeros(test_frames[0].shape, dtype=np.uint8))
        test_frames = np.array(test_frames[:max_frames])  # Преобразование к массиву кадров

        prediction = self.model.predict(np.array([test_frames]))  # Предсказание
        print(prediction[0])
        if prediction[0] < 0.3:
            result = "Real Video"
        else:
            result = "Deepfake Video"

        print("The video is:", result)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
