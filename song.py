# song.py

class Song:
    def __init__(self, filename, artist, title, release_date, tags,user_id=None):
        self.filename = filename
        self.artist = artist
        self.title = title
        self.release_date = release_date
        self.tags = tags
        self.user_id = user_id

    def __str__(self):
        return f"{self.title} by {self.artist} ({self.release_date}) - Tags: {', '.join(self.tags)}"
