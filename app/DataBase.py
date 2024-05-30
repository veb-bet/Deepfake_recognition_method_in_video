import sqlite3


class DataBase:
    def __init__(self, name):
        # telling name of .db-file on init
        self.name = name
        # DataBase object holds requisites of user, who uses this database at the moment.
        # basically, this class could be named "Account" if it needed for anything else, but communicating with DB.
        self.id = None
        self.nickname = None
        self.password = None
        self.icon = None

    # if file doesn't exist yet, this function should be activated.
    # run this file `python DataBase.py` to create database file.
    def create_new_db_file(self):
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            # Passwords have fantastic informational security
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nickname TEXT UNIQUE NOT NULL,
                    Password TEXT NOT NULL,
                    Icon BLOB
                );
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Requests (
                    Date TEXT PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Video BLOB NOT NULL,
                    IsFake INTEGER NOT NULL,
                    FakeCoefficient REAL NOT NULL,
                    UserID INTEGER,
                    Feedback TEXT,
                    FOREIGN KEY (UserID) REFERENCES Users (ID) ON DELETE CASCADE
                );
            ''')

    # USERS
    def registration(self, nickname, password):
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            cursor.execute(
                '''INSERT INTO Users (Nickname, Password, Icon) VALUES (?, ?, ?) ON CONFLICT (Nickname) DO NOTHING''',
                (nickname, password, None))

    def login(self, nickname, password):
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            res = cursor.execute('''SELECT (ID) FROM Users WHERE Nickname =? and Password =?''',
                                 (nickname, password)).fetchone()
            self.id = res[0] if res else None
        if self.id:
            self.nickname = nickname
            self.password = password
            self.icon = self.get_icon()

    def get_icon(self):
        if self.id:
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                res = cursor.execute('''SELECT (Icon) FROM Users WHERE ID = ?''', (self.id,)).fetchone()
                return res[0] if res else None

    def logout(self):
        self.id = None
        self.nickname = None
        self.password = None
        self.icon = None

    def change_nickname(self, new_nickname):
        if self.id and new_nickname != "":
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                cursor.execute('''UPDATE Users SET Nickname = ? WHERE ID =?''', (new_nickname, self.id))

    def change_password(self, new_password):
        if self.id and new_password != "":
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                cursor.execute('''UPDATE Users SET Password = ? WHERE ID =?''', (new_password, self.id))

    def change_icon(self, new_icon):
        if self.id:
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                cursor.execute('''UPDATE Users SET Icon = ? WHERE ID =?''', (new_icon, self.id))

    def delete_user(self):
        if self.id:
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                cursor.execute('''DELETE FROM Users WHERE ID =?''', (self.id,))
            self.logout()

    # REQUESTS
    # get whole history from Request table
    def read_history(self):
        if self.id:
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                return cursor.execute("SELECT Date, Name, IsFake, FakeCoefficient, Feedback FROM Requests").fetchall()

    # get single request on specific datetime.
    def read_video(self, date):
        if self.id:
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                return cursor.execute("SELECT Video FROM Requests WHERE Date = ? AND UserID = ?",
                                      (date, self.id)).fetchone()[0]

    # add single request in the Request
    def add_request(self, date, name, video, is_fake, fake_coefficient, feedback):
        if self.id:
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    '''INSERT INTO Requests (Date, Name, Video, IsFake, FakeCoefficient, UserId, Feedback) 
                        VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT (DATE) DO NOTHING''',
                    (date, name, video, is_fake, fake_coefficient, self.id, feedback))

    # remove single request on specific date
    def remove_single_request(self, date):
        if self.id:
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Requests WHERE Date = ?", (date,))


if __name__ == "__main__":
    db = DataBase(name='DeepFakeDataBase.db')
    db.create_new_db_file()
