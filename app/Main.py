import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget

from DataBase import DataBase
from ProfileTab import ProfileTab
from AnalysisTab import AnalysisTab
from HistoryTab import HistoryTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("deepfake detector")
        self.setGeometry(50, 50, 700, 400)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.tabs = QTabWidget()
        self.central_layout.addWidget(self.tabs)

        self.DataBase = DataBase('DeepFakeDataBase.db')

        self.profile_tab = ProfileTab(self.DataBase)
        self.analyze_tab = AnalysisTab(self.DataBase)
        self.history_tab = HistoryTab(self.DataBase)
        self.tabs.addTab(self.profile_tab, "Профиль")
        self.tabs.addTab(self.analyze_tab, "Анализ")
        self.tabs.addTab(self.history_tab, "История")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
