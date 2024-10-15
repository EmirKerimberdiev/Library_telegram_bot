import sqlite3


# connection = sqlite3.connect("db.sqlite")
class Database:
    def __init__(self, path):
        self.path = path

    def create_table(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS survey_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    tg_id INTEGER,
                    genre TEXT
                )
            """)

            connection.commit()


database = Database("db.sqlite")
database.create_table()
