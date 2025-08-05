from tkinter import *
from Database import Database
from song_storage import SongStorage
from song import Song
from tkinter import filedialog
import os
import re
from delete import SongListView
import shutil
from tkinter import messagebox

def clean_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '', name)
class SongApp:
    def __init__(self,root,db,user_id):
        self.file_path = None
        self.root=root
        self.user_id=user_id
        self.root.title("Playlist")
        self.root.geometry("400x600")
        self.root.resizable(0, 0)
        self.root.configure(bg="deep sky blue")
        self.patrat = Frame(self.root, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat.place(x=20, y=20)
        self.db=db
        heading=Label(self.patrat, text="ADD A SONG",font=("Microsoft Yahei UI Light",23,'bold'),bg="white",fg="DeepSkyBlue2")
        heading.place(x=80,y=40)
        self.entry_adauga_fisier = Entry(self.patrat, font=("Microsoft Yahei UI Light",12,'bold'), width=12,disabledbackground="DeepSkyBlue2",
    disabledforeground="white", bd=2)
        self.entry_adauga_fisier.insert(0, "Adauga fisier:")
        self.entry_adauga_fisier.place(x=20,y=150)
        self.entry_adauga_fisier.config(state="disabled")
        frame_adauga = Frame(self.patrat, bg="DeepSkyBlue2", bd=0)
        frame_adauga.place(x=145, y=150)
        self.adauga_button = Button(
            frame_adauga,
            font=("Microsoft Yahei UI Light", 12, 'bold'),
            command=self.adauga_fis,
            width=19,
            bg="white",
            fg="black",
            bd=0,
            relief="flat",
            activebackground="white",
            activeforeground="black"
        )
        self.adauga_button.pack(padx=2, pady=2)

        self.entry_file_name = Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold'),width=12,disabledbackground="DeepSkyBlue2",
    disabledforeground="white", bd=2)
        self.entry_file_name.insert(0, "File name:")
        self.entry_file_name.place(x=20,y=200)
        self.entry_file_name.config(state="disabled")
        self.entry_file_name_utilizator = Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold') ,bd=0,highlightthickness=2,
    highlightbackground="DeepSkyBlue2",
    highlightcolor="sky blue")
        self.entry_file_name_utilizator.place(x=145,y=200)

        self.entry_artist = Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold'),width=12,disabledbackground="DeepSkyBlue2",
    disabledforeground="white", bd=2)
        self.entry_artist.insert(0, "Artist: ")
        self.entry_artist.place(x=20,y=250)
        self.entry_artist.config(state="disabled")
        self.entry_artist_utilizator=Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold'),bd=0, highlightthickness=2,
    highlightbackground="DeepSkyBlue2",
    highlightcolor="sky blue")
        self.entry_artist_utilizator.place(x=145,y=250)

        self.entry_title = Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold'),width=12,disabledbackground="DeepSkyBlue2",
    disabledforeground="white", bd=2)
        self.entry_title.insert(0, "Title: ")
        self.entry_title.place(x=20,y=300)
        self.entry_title.config(state="disabled")
        self.entry_title_utilizator=Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold'),bd=0, highlightthickness=2,
    highlightbackground="DeepSkyBlue2",
    highlightcolor="sky blue")
        self.entry_title_utilizator.place(x=145,y=300)

        self.entry_release_date = Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold'),width=12,disabledbackground="DeepSkyBlue2",
    disabledforeground="white", bd=2)
        self.entry_release_date.insert(0, "Release date: ")
        self.entry_release_date.place(x=20,y=350)
        self.entry_release_date.config(state="disabled")
        self.entry_release_date_utilizator=Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold'),bd=0, highlightthickness=2,
    highlightbackground="DeepSkyBlue2",
    highlightcolor="sky blue")
        self.entry_release_date_utilizator.place(x=145,y=350)

        self.entry_tags=Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold'),width=12,disabledbackground="DeepSkyBlue2",
    disabledforeground="white", bd=2)
        self.entry_tags.insert(0, "Tags:  ")
        self.entry_tags.place(x=20,y=400)
        self.entry_tags.config(state="disabled")
        self.entry_tags_utilizator=Entry(self.patrat,font=("Microsoft Yahei UI Light",12,'bold'),bd=0, highlightthickness=2,
    highlightbackground="DeepSkyBlue2",
    highlightcolor="sky blue")
        self.entry_tags_utilizator.place(x=145,y=400)

        self.save_button = Button(self.patrat, text="Salvează", command=self.save_song,font=("Microsoft Yahei UI Light",22,'bold'),bg='deep sky blue',fg='white',activeforeground='white',activebackground='SkyBlue1')
        self.save_button.place(x=100,y=450)
    def adauga_fis(self):
         self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
         if not self.file_path:
             return
         filename_only = os.path.basename(self.file_path)
         self.adauga_button.config(text=filename_only)
    def save_song(self):
        if not self.file_path:
            print("⚠️ Nu ai selectat niciun fișier!")
            return
        original_ext = os.path.splitext(self.file_path)[1]
        filename = clean_filename(self.entry_file_name_utilizator.get())
        if not filename:
            print("⚠️ Numele fișierului nu poate fi gol!")
            return
        if not filename.endswith(original_ext):
            filename += original_ext
        artist = self.entry_artist_utilizator.get()
        title = self.entry_title_utilizator.get()
        release_date = self.entry_release_date_utilizator.get()
        tags_raw = self.entry_tags_utilizator.get()
        tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]
        song = Song(filename, artist, title, release_date, tags, self.user_id)
        storage = SongStorage(self.db)
        dest_path = os.path.join(storage.storage_folder, filename)
        os.makedirs(storage.storage_folder, exist_ok=True)
        shutil.copy(self.file_path, dest_path)
        storage.add_song(song, dest_path)
        print(f"🎵 Salvat: {title} by {artist}")
        messagebox.showinfo("Felicitari", "Felicitari, ai adaugat un cantec!")
        self.root.destroy()
    def deschide_lista(self):
        new_window = Toplevel(self.root)
        SongListView(new_window)