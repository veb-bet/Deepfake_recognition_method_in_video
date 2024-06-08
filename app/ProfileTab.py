from PyQt5.QtWidgets import QWidget,  QVBoxLayout, QGroupBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
                            QMessageBox, QInputDialog, QFileDialog
from PyQt5.QtGui import QPixmap


class ProfileTab(QWidget):
    def __init__(self, database):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.database = database

        # Auth section
        self.auth_box = QGroupBox()
        layout.addWidget(self.auth_box)
        auth_layout = QGridLayout()
        self.auth_box.setLayout(auth_layout)

        nickname_label = QLabel("Логин")
        self.nickname_line = QLineEdit()
        password_label = QLabel("Пароль")
        self.password_line = QLineEdit()
        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.on_login_btn_clicked)
        registration_button = QPushButton("Зарегистрироваться")
        registration_button.clicked.connect(self.on_registration_btn_clicked)

        auth_layout.addWidget(nickname_label, 0, 0, 1, 1)
        auth_layout.addWidget(self.nickname_line, 0, 1, 1, 3)
        auth_layout.addWidget(password_label, 1, 0, 1, 1)
        auth_layout.addWidget(self.password_line, 1, 1, 1, 3)
        auth_layout.addWidget(login_button, 2, 0, 1, 4)
        auth_layout.addWidget(registration_button, 3, 0, 1, 4)

        # Account section
        self.account_box = QGroupBox()
        layout.addWidget(self.account_box)
        account_layout = QGridLayout()
        self.account_box.setLayout(account_layout)

        # picture
        self.icon_image = QLabel()
        pixmap = QPixmap("data/images/icon.png").scaled(100, 100)
        self.icon_image.setPixmap(pixmap)
        self.icon_image.setContentsMargins(50, 0, 0, 0)
        change_icon_button = QPushButton("Сменить иконку профиля")
        change_icon_button.clicked.connect(self.on_change_icon_btn_clicked)
        # nickname
        self.nickname_text = QLabel()
        self.nickname_text.setContentsMargins(70, 0, 0, 0)
        font = self.nickname_text.font()
        font.setBold(True)
        self.nickname_text.setFont(font)
        # btns
        change_nickname_button = QPushButton("Изменить никнейм")
        change_nickname_button.clicked.connect(self.on_change_nickname_btn_clicked)
        change_password_button = QPushButton("Изменить пароль")
        change_password_button.clicked.connect(self.on_change_password_btn_clicked)
        delete_user_button = QPushButton("Удалить аккаунт")
        delete_user_button.clicked.connect(self.on_delete_user_btn_clicked)
        logout_button = QPushButton("Выйти из приложения")
        logout_button.clicked.connect(self.on_logout_btn_clicked)

        account_layout.addWidget(self.icon_image, 0, 0, 4, 1)
        account_layout.addWidget(self.nickname_text, 4, 0)
        account_layout.addWidget(change_icon_button, 0, 1)
        account_layout.addWidget(change_nickname_button, 1, 1)
        account_layout.addWidget(change_password_button, 2, 1)
        account_layout.addWidget(delete_user_button, 3, 1)
        account_layout.addWidget(logout_button, 4, 1)

        self.account_box.hide()

    def on_login_btn_clicked(self):
        self.database.login(self.nickname_line.text(), self.password_line.text())
        if self.database.id:
            self.nickname_text.setText(self.database.nickname)

            if self.database.icon:
                with open('temp/current_icon.jpg', 'wb') as file:
                    file.write(self.database.icon)
                icon = QPixmap('temp/current_icon.jpg').scaled(100, 100)
                self.icon_image.setPixmap(icon)
            else:
                icon = QPixmap('data/images/icon.png').scaled(100, 100)
                self.icon_image.setPixmap(icon)

            self.auth_box.hide()
            self.account_box.show()
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("Ошибка аутентификации")
            message_box.setText("Такой аккаунт не существует, либо пароль не действителен.\nПопробуйте ещё.")
            message_box.setIcon(QMessageBox.Warning)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.setDefaultButton(QMessageBox.Ok)
            message_box.exec()

    def on_registration_btn_clicked(self):
        self.database.registration(self.nickname_line.text(), self.password_line.text())
        message_box = QMessageBox()
        message_box.setWindowTitle("Создание аккаунта")
        message_box.setText("Аккаунт успешно создан. Теперь вы можете войти.")
        message_box.setIcon(QMessageBox.Information)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.setDefaultButton(QMessageBox.Ok)
        message_box.exec()

    def on_change_icon_btn_clicked(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите картинку", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            with open(file_path, 'rb') as icon:
                self.database.change_icon(icon.read())
            new_icon = QPixmap(file_path).scaled(100, 100)
            self.icon_image.setPixmap(new_icon)

    def on_change_nickname_btn_clicked(self):
        new_nickname, ok = QInputDialog.getText(self, "Сменить имя пользователя", "Введите новое имя пользователя:")
        if ok and new_nickname:
            self.database.change_nickname(new_nickname)
            self.nickname_text.setText(new_nickname)

    def on_change_password_btn_clicked(self):
        new_password, ok = QInputDialog.getText(self, "Сменить пароль пользователя", "Введите новый пароль:")
        if ok and new_password:
            self.database.change_password(new_password)

    def on_delete_user_btn_clicked(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Подтверждение удаления аккаунта")
        message_box.setText("Вы уверены, что хотите удалить аккаунт?")
        message_box.setIcon(QMessageBox.Warning)
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)
        reply = message_box.exec()
        if reply == QMessageBox.Yes:
            self.database.delete_user()
            message_box.setWindowTitle("")
            message_box.setText("Аккаунт успешно удалён.")
            self.auth_box.show()
            self.account_box.hide()

    def on_logout_btn_clicked(self):
        self.database.logout()
        self.auth_box.show()
        self.account_box.hide()


