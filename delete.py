# song_list_view.py
from tkinter import *
from song_storage import SongStorage
import pygame
import time
class SongListView:
    def __init__(self, root, db,user_id):
        self.root = root
        self.user_id=user_id
        pygame.mixer.init()
        self.root.title("Melodii salvate")
        self.root.geometry("400x600")
        self.db = db
        self.root.resizable(0, 0)
        self.storage = SongStorage(self.db)
        self.root.configure(bg="SpringGreen4")
        self.patrat = Frame(self.root, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat.place(x=20, y=20)


        heading=Label(self.patrat, text="Recorded Songs", font=("Microsoft Yahei UI Light",23,'bold'),bg="white",fg="Green3")
        heading.place(x=70,y=30)

        self.listbox = Listbox(self.patrat, width=33,height=15,font=("Microsoft Yahei UI Light",12,'bold'),bg='PaleGreen',selectbackground='Green4')
        self.listbox.place(x=10,y=110)
        scrollbar = Scrollbar(self.patrat, orient="vertical")
        scrollbar.place(x=330, y=110, height=340)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        self.save=Button(self.patrat, text="Clear Selection", command=self.delete_selected,font=("Microsoft Yahei UI Light",20,'bold'),bg='green3',activebackground='palegreen',activeforeground='white')
        self.save.place(x=70,y=480)

        self.load_songs()

    def load_songs(self):
        self.listbox.delete(0, END)
        songs = self.storage.get_all_songs(self.user_id)
        for song in songs:
            song_id, title, artist = song[0], song[3], song[4]
            self.listbox.insert(END, f"{song_id}. {title} by {artist}")

    def delete_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            print("⚠️ Selectează o melodie de șters.")
            return
        index = selection[0]
        entry = self.listbox.get(index)
        song_id = int(entry.split(".")[0])
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        time.sleep(0.1)  # 100 ms delay
        self.storage.delete_song(song_id)
        self.load_songs()

        print(f"🗑️ Șters melodia cu ID {song_id}")
