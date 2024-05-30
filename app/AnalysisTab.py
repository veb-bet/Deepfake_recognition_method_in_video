from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit, QMessageBox
from Analysis import Analysis

class AnalysisTab(QWidget):
    def __init__(self, database):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.database = database
        self.analysis = Analysis()
        self.video_name = None

        # Upload
        upload_button = QPushButton("Загрузить видео")
        upload_button.clicked.connect(self.on_upload_btn_clicked)
        layout.addWidget(upload_button)

        self.upload_label = QLabel()
        layout.addWidget(self.upload_label)

        analyze_button = QPushButton("Проанализировать")
        analyze_button.clicked.connect(self.on_analyze_btn_clicked)
        layout.addWidget(analyze_button)

        self.analysis_result_label = QLabel("")
        font = self.analysis_result_label.font()
        font.setBold(True)
        self.analysis_result_label.setFont(font)
        layout.addWidget(self.analysis_result_label)

        feedback_label = QLabel("Оставьте комментарий:")
        layout.addWidget(feedback_label)

        self.feedback = QTextEdit("")
        layout.addWidget(self.feedback)

        save_button = QPushButton("Сохранить результат")
        save_button.clicked.connect(self.on_save_btn_clicked)
        layout.addWidget(save_button)

    def extract_filename(self, path):
        file = path.rsplit("/", 1)
        return file[-1] if len(path) > 1 else path

    def on_upload_btn_clicked(self):
        file_dialog = QFileDialog()
        video_path, _ = file_dialog.getOpenFileName(self, "Выберите видео", "", "Video Files (*.mp4 *.avi)")
        with open(video_path, "rb") as video:
            self.analysis.video = video.read()
        self.analysis_result_label.setText("")
        self.video_name = self.extract_filename(video_path)
        self.upload_label.setText(f"Загружено: {self.video_name}")

    def on_analyze_btn_clicked(self):
        if self.analysis.video:
            self.analysis.analyze()
            result = "Video is fake" if self.analysis.is_fake else "Video is real"
            result += ", fake_coefficent: " + str(self.analysis.fake_coefficient)
            self.analysis_result_label.setText(result)
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("Ошибка")
            message_box.setText("Сначала загрузите видео!")
            message_box.setIcon(QMessageBox.Warning)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.setDefaultButton(QMessageBox.Ok)
            message_box.exec()

    def on_save_btn_clicked(self):
        if self.analysis.fake_coefficient:
            self.database.add_request(date=self.analysis.request_time, name=self.video_name, video=self.analysis.video,
                                      is_fake=1 if self.analysis.is_fake else 0,
                                      fake_coefficient=float(self.analysis.fake_coefficient),
                                      feedback=self.feedback.toPlainText())
            self.video_name = None
            self.analysis.clear_result()

            self.upload_label.setText("")
            message_box = QMessageBox()
            message_box.setWindowTitle("Сохранение")
            message_box.setText("Запрос успешно сохранён.")
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.setDefaultButton(QMessageBox.Ok)
            message_box.exec()
