
import os
from song import Song
class SongStorage:
    def __init__(self, db, storage_folder="storage"):
        self.db = db
        self.cursor = db.cursor
        self.storage_folder = storage_folder
        os.makedirs(self.storage_folder, exist_ok=True)

    def add_song(self, song, file_path):
        self.cursor.execute("""
                            INSERT INTO song (user_id,filename, artist, title, release_date, tags)
                            VALUES (%s,%s, %s, %s, %s, %s)
                            """, (song.user_id,song.filename, song.artist, song.title, song.release_date, ",".join(song.tags)))
        self.db.conn.commit()

    def delete_song(self, song_id):
        self.cursor.execute("SELECT filename FROM song WHERE id = %s", (song_id,))
        result = self.cursor.fetchone()
        if result:
            file_path = os.path.join(self.storage_folder, result[0])
            if os.path.exists(file_path):
                os.remove(file_path)
            self.cursor.execute("DELETE FROM song WHERE id = %s", (song_id,))
            self.db.conn.commit()

    def search_songs(self, field, value):
        self.cursor.execute(f"SELECT * FROM song WHERE {field} LIKE %s", (f"%{value}%",))
        return self.cursor.fetchall()

    def update_metadata(self, song_id, field, new_value):
        self.cursor.execute(f"UPDATE song SET {field} = %s WHERE id = %s", (new_value, song_id))
        self.db.conn.commit()

    def get_all_songs(self, user_id=None):
        cursor = self.db.cursor
        if user_id is not None:
            cursor.execute("SELECT id,user_id,filename, artist, title,release_date,tags FROM song WHERE user_id = %s",
                           (user_id,))
        else:
            cursor.execute("SELECT id,user_id,filename, artist, title,release_date,tags FROM song")
        return cursor.fetchall()

    def update_song_metadata(self, song_id, song):
        query = """
                UPDATE song
                SET artist       = %s,
                    title        = %s, 
                    release_date = %s, 
                    tags         = %s
                WHERE id = %s 
                """
        tags_str = ",".join(song.tags)
        self.cursor.execute(query, (song.artist, song.title, song.release_date, tags_str, song_id))
        self.db.conn.commit()

    def get_all_songs_full(self):
        self.cursor.execute("SELECT * FROM song")
        return self.cursor.fetchall()

