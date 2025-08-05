from tkinter import *
from song_storage import SongStorage
from tkinter import messagebox
class SearchWindow:
    def __init__(self, parent, db,user_id):
        self.db = db
        self.storage = SongStorage(self.db)
        self.user_id = user_id
        self.root = Toplevel(parent)
        self.root.title("Caută melodii")
        self.root.geometry("400x600")
        self.root.resizable(0, 0)
        self.root.configure(bg="wheat4")
        self.patrat = Frame(self.root, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat.place(x=20, y=20)

        Label(self.patrat, text="Title:",font=("Microsoft Yahei UI Light",11,'bold'),bd=2,background='burlywood4',fg='white',width=12).place(x=20, y=40)
        self.title_var = StringVar()
        Entry(self.patrat, textvariable=self.title_var,font=("Microsoft Yahei UI Light",11,'bold'),width=23,bd=0,highlightthickness=2,
    highlightbackground="burlywood4",
    highlightcolor="burlywood4").place(x=130, y=40)

        Label(self.patrat, text="Artist:",font=("Microsoft Yahei UI Light",11,'bold'),bd=2,bg='burlywood4',fg='white',width=12).place(x=20, y=80)
        self.artist_var = StringVar()
        Entry(self.patrat, textvariable=self.artist_var,font=("Microsoft Yahei UI Light",11,'bold'),bd=0,highlightthickness=2,
    highlightbackground="burlywood4",
    highlightcolor="burlywood4",width=23).place(x=130, y=80)

        Label(self.patrat, text="Tag:",font=("Microsoft Yahei UI Light",11,'bold'),bd=2,bg='burlywood4',fg='white',width=12).place(x=20, y=120)
        self.tag_var = StringVar()
        Entry(self.patrat, textvariable=self.tag_var,font=("Microsoft Yahei UI Light",11,'bold'),bd=0,highlightthickness=2,
    highlightbackground="burlywood4",
    highlightcolor="burlywood4",width=23).place(x=130, y=120)
        Label(self.patrat, text="Release Date:",font=("Microsoft Yahei UI Light",11,'bold'),bd=2,bg='burlywood4',fg='white',width=12).place(x=20, y=160)
        self.release_var = StringVar()
        Entry(self.patrat, textvariable=self.release_var,bd=0,highlightthickness=2,
    highlightbackground="burlywood4",
    highlightcolor="burlywood4",font=("Microsoft Yahei UI Light",11,'bold'),width=23).place(x=130, y=160)

        Button(self.patrat, text="Search", command=self.search,font=("Microsoft Yahei UI Light",18,'bold'),bg='burlywood4',fg='white',activebackground='burlywood1',activeforeground='white').place(x=120,y=220)

        self.result_listbox = Listbox(self.patrat, width=35,font=("Microsoft Yahei UI Light",11,'bold'),background='LightYellow2',selectbackground='PeachPuff4')
        self.result_listbox.place(x=20,y=300)
        scrollbar = Scrollbar(self.patrat, orient='vertical')
        scrollbar.place(x=330, y=300, height=210)

        self.result_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_listbox.yview)

    def search(self):
        title = self.title_var.get().strip().lower()
        artist = self.artist_var.get().strip().lower()
        tag = self.tag_var.get().strip().lower()
        release_date = self.release_var.get().strip().lower()

        if not (title or artist or tag or release_date):
            messagebox.showwarning("Căutare invalidă", "Completează cel puțin un câmp pentru a căuta.")
            return

        self.result_listbox.delete(0, END)
        all_songs = self.storage.get_all_songs(self.user_id)
        print(all_songs)  # DEBUG

        for song in all_songs:
            song_id, song_artist, song_title, release, tags = song[0], song[3], song[4], song[5], song[6]

            release_str = str(release) if release else ""
            tags_str = tags if isinstance(tags, str) else ""
            tags_list = [t.strip().lower() for t in tags_str.split(',')]

            print(f"Titlu: {song_title}, Artist: {song_artist}, Release: {release_str}, Tags: {tags_str}")  # DEBUG

            match = (
                    (title and title in song_title.lower()) or
                    (artist and artist in song_artist.lower()) or
                    (release_date and release_date in release_str.lower()) or
                    (tag and any(tag in t for t in tags_list))
            )

            if match:
                self.result_listbox.insert(
                    END,
                    f"{song_id}. {song_title} - {song_artist} | {release_str} | Tags: {tags_str}"
                )
