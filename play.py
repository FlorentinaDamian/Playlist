import pygame
from tkinter import *
from song_storage import SongStorage
import os
class PlayWindow:
    def __init__(self, root, db,user_id):
        self.user_id=user_id
        self.db = db
        self.root = root
        self.root.title("Player")
        self.root.geometry("400x600")
        self.root.resizable(0, 0)
        self.root.configure(background="DodgerBlue4")
        pygame.mixer.init()
        self.patrat = Frame(self.root, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat.place(x=20, y=20)
        heading = Label(self.patrat, text="Select a Song", font=("Microsoft Yahei UI Light", 23, 'bold'), bg="white",
                        fg="DodgerBlue4")
        heading.place(x=70, y=20)

        self.listbox = Listbox(self.patrat, width=35, font=("Microsoft Yahei UI Light",11,'bold'),bg='light blue')
        self.listbox.place(x=20,y=90)
        scrollbar = Scrollbar(self.patrat, orient='vertical')
        scrollbar.place(x=330, y=90, height=210)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.play_button = Button(self.patrat, text="Play", command=self.play_selected,font=("Microsoft Yahei UI Light",13,'bold'),width=28,bg='RoyalBlue4',fg='white',activeforeground='white',activebackground='cornflower blue')
        self.play_button.place(x=20,y=330)

        self.pause_button = Button(self.patrat, text="Pause", command=self.pause,font=("Microsoft Yahei UI Light",13,'bold'),width=28,bg='RoyalBlue4',fg='white',activeforeground='white',activebackground='cornflower blue')
        self.pause_button.place(x=20,y=380)

        self.resume_button = Button(self.patrat, text="Resume", command=self.resume,font=("Microsoft Yahei UI Light",13,'bold'),width=28,bg='RoyalBlue4',fg='white',activeforeground='white',activebackground='cornflower blue')
        self.resume_button.place(x=20,y=430)

        self.stop_button = Button(self.patrat, text="Stop", command=self.stop,font=("Microsoft Yahei UI Light",13,'bold'),width=28,bg='RoyalBlue4',fg='white',activeforeground='white',activebackground='cornflower blue')
        self.stop_button.place(x=20,y=480)

        self.storage = SongStorage(self.db)
        self.songs = []
        self.current_song_path = None
        self.is_paused = False
        self.load_songs()

    def load_songs(self):
        self.songs = self.storage.get_all_songs(self.user_id)
        self.listbox.delete(0, END)
        for song in self.songs:
            song_id, artist, title = song[0], song[3], song[4]
            self.listbox.insert(END, f"{song_id}. {title} - {artist}")

    def play_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            print("⚠️ Selectează o melodie.")
            return

        index = selection[0]
        song = self.songs[index]
        self.current_song_path = song[2]
        storage_folder = "storage"
        self.current_song_path = os.path.join(storage_folder, self.current_song_path)
        try:
            pygame.mixer.music.load(self.current_song_path)
            pygame.mixer.music.play()
            print("▶️ Se redă:", self.current_song_path)
        except Exception as e:
            print("Eroare la redare:", e)

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True

    def resume(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop(self):
        pygame.mixer.music.stop()
