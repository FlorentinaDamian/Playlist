from tkinter import *
from song_storage import SongStorage
from song import Song

class EditSongsWindow:
    def __init__(self, parent, db,user_id):
        self.db = db
        self.user_id=user_id
        self.storage = SongStorage(self.db)
        self.root = Toplevel(parent)  # fereastră separată
        self.root.title("Editează Melodii")
        self.root.geometry("400x600")
        self.root.resizable(0, 0)
        self.selected_song_id = None
        self.root.configure(bg="deep pink")
        self.patrat = Frame(self.root, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat.place(x=20, y=20)

        header=Label(self.patrat, text="Songs Available",font=("Microsoft Yahei UI Light",23,'bold'),bg="white",fg='maroon1')
        header.place(x=60, y=20)

        self.listbox = Listbox(self.patrat, width=35,font=("Microsoft Yahei UI Light",11,'bold'),bg='pink',selectbackground='HotPink4')
        self.listbox.place(x=20, y=80)
        self.listbox.bind("<<ListboxSelect>>", self.on_song_select)
        scrollbar = Scrollbar(self.patrat, orient="vertical")
        scrollbar.place(x=330, y=80, height=210)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        self.title_var = StringVar()
        self.artist_var = StringVar()
        self.release_var = StringVar()
        self.tags_var = StringVar()

        Label(self.patrat,width=12, text="Title:",font=("Microsoft Yahei UI Light",11,'bold'),bg='violet red',fg='white',bd=2).place(x=20, y=300)
        self.entry_title = Entry(self.patrat, textvariable=self.title_var, width=21,font=("Microsoft Yahei UI Light",11,'bold'),bd=0,highlightthickness=2,
    highlightbackground="violet red",  # culoarea când NU e focusat
    highlightcolor="violet red")
        self.entry_title.place(x=140, y=300)

        Label(self.patrat,width=12, text="Artist:",font=("Microsoft Yahei UI Light",11,'bold'),bg='violet red',fg='white',bd=2).place(x=20, y=350)
        self.entry_artist = Entry(self.patrat, textvariable=self.artist_var, width=21,font=("Microsoft Yahei UI Light",11,'bold'),bd=0,highlightthickness=2,
    highlightbackground="violet red",  # culoarea când NU e focusat
    highlightcolor="violet red")
        self.entry_artist.place(x=140, y=350)

        Label(self.patrat,width=12, text="Release date:",font=("Microsoft Yahei UI Light",11,'bold'),bg='violet red',fg='white',bd=2).place(x=20, y=400)
        self.entry_release = Entry(self.patrat, textvariable=self.release_var, width=21,font=("Microsoft Yahei UI Light",11,'bold'),bd=0,highlightthickness=2,
    highlightbackground="violet red",  # culoarea când NU e focusat
    highlightcolor="violet red")
        self.entry_release.place(x=140, y=400)

        Label(self.patrat,width=12, text="Tags:",font=("Microsoft Yahei UI Light",11,'bold'),bg='violet red',fg='white',bd=2).place(x=20, y=450)
        self.entry_tags = Entry(self.patrat, textvariable=self.tags_var, width=21,font=("Microsoft Yahei UI Light",11,'bold'),bd=0,highlightthickness=2,
    highlightbackground="violet red",  # culoarea când NU e focusat
    highlightcolor="violet red")
        self.entry_tags.place(x=140, y=450)

        Button(self.patrat, text="Save", command=self.save_changes,font=("Microsoft Yahei UI Light",17,'bold'),bg='DeepPink4',fg='white',activebackground='HotPink3').place(x=140, y=490)

        self.load_songs()

    def load_songs(self):
        self.listbox.delete(0, END)
        self.songs = self.storage.get_all_songs(self.user_id)
        for song in self.songs:
            song_id, user_id,filename, artist, title, release_date, tags = song
            tags_display = tags if tags else "-"
            self.listbox.insert(END, f"{song_id}. {title} - {artist}_{release_date}_{tags_display}")

    def on_song_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        song_data = self.songs[index]
        self.selected_song_id = song_data[0]
        self.artist_var.set(song_data[3])
        self.title_var.set(song_data[4])
        self.release_var.set(song_data[5])

        tags_raw = song_data[6]
        if isinstance(tags_raw, str) and "," in tags_raw:
            self.tags_var.set(", ".join([t.strip() for t in tags_raw.split(",")]))
        elif isinstance(tags_raw, str):
            self.tags_var.set(tags_raw.strip())
        else:
            self.tags_var.set("")

    def save_changes(self):
        if self.selected_song_id is None:
            print("⚠️ Nicio melodie selectată.")
            return

        title = self.title_var.get()
        artist = self.artist_var.get()
        release_date = self.release_var.get()
        tags_raw = self.tags_var.get()
        tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]

        original_song = next((s for s in self.songs if s[0] == self.selected_song_id), None)
        filename = original_song[2] if original_song else ""

        song = Song(filename, artist, title, release_date, tags,self.user_id)
        self.storage.update_song_metadata(self.selected_song_id, song)
        print(f"✅ Melodia cu ID {self.selected_song_id} a fost actualizată.")
        self.load_songs()
