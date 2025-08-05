
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=r"C:\Users\damia\Desktop\Proicte_Cv\Python\Playlist\.env")
password=os.getenv("PASSWORD")
print("Parola încărcată:", password)
class Database:
    def __init__(self, user='root', passwd=None, host='localhost'):
        if passwd is None:
            passwd = os.getenv("PASSWORD")
        self.conn = mysql.connector.connect(
            user=user,
            passwd=passwd,  # folosește parametrul corect aici
            host=host
        )
        self.cursor = self.conn.cursor()
        self._init_database()

    def column_exists(self, table_name, column_name):
        self.cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = 'song_storage'
              AND TABLE_NAME = '{table_name}'
              AND COLUMN_NAME = '{column_name}'
        """)
        return self.cursor.fetchone()[0] == 1
    def _init_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS song_storage")
        self.cursor.execute("USE song_storage")
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users
                            (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(50) UNIQUE,
                                password VARCHAR(255)
                                )
                            """)
        if not self.column_exists('users', 'email'):
            self.cursor.execute("ALTER TABLE users ADD COLUMN email VARCHAR(255)")
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS song
                            (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                filename VARCHAR(255),
                                artist VARCHAR(100),
                                title VARCHAR(100),
                                release_date DATE,
                                tags TEXT,
                                user_id INT,
                                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                                )
                            """)
        self.conn.commit()
    def commit(self):
        self.conn.commit()
    def close(self):
        self.cursor.close()
        self.conn.close()
