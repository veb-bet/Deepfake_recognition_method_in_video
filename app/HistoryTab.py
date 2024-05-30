from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from functools import partial
import cv2


class HistoryTab(QWidget):
    def __init__(self, database):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.table = QTableWidget()
        layout.addWidget(self.table)

        update_history_button = QPushButton("Обновить историю запросов")
        update_history_button.clicked.connect(self.update_history)
        layout.addWidget(update_history_button)

        self.database = database

        self.update_history()

    def update_history(self):
        self.table.clear()
        self.table.setColumnCount(7)
        # Date Name Video IsFake FakeCoefficient Feedback
        self.table.setHorizontalHeaderLabels(
            ["Дата запроса", "Название", "Статус", "Коэффициент", "Фидбек", "", ""])

        requests = self.database.read_history()
        if requests:

            # while self.table.rowCount() > 0:
            #     self.table.removeRow(0)
            self.table.setRowCount(len(requests))
            # for i in range(6):
            #     self.table.setItem(0, i, QTableWidgetItem(" - "))
            i = 0
            for request in requests:
                # Date Name Video IsFake FakeCoefficient UserID Feedback
                self.table.setItem(i, 0, QTableWidgetItem(request[0]))                          # Date
                self.table.setItem(i, 1, QTableWidgetItem(request[1]))                          # Name
                self.table.setItem(i, 2, QTableWidgetItem("Fake" if request[2] else "Real"))    # IsFake
                self.table.setItem(i, 3, QTableWidgetItem(str(request[3])))                     # FakeCoefficient
                self.table.setItem(i, 4, QTableWidgetItem(request[4]))                          # Feedback
                watch_item = QPushButton("watch")
                watch_item.clicked.connect(partial(self.watch_video, request[0]))
                self.table.setCellWidget(i, 5, watch_item)
                delete_item = QPushButton("delete")
                delete_item.clicked.connect(partial(self.delete_request, request[0]))
                self.table.setCellWidget(i, 6, delete_item)

                i += 1

    def watch_video(self, date):
        video = self.database.read_video(date)
        if video:
            with open('temp/watched_video.mp4', 'wb') as file:
                file.write(video)
            cap = cv2.VideoCapture('temp/watched_video.mp4')
            while True:
                ret, frame = cap.read()
                if ret:
                    cv2.imshow("press q to quit", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()

    def delete_request(self, date):
        self.database.remove_single_request(date)
        self.update_history()
