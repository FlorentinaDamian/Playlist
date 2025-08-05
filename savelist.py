from tkinter import *
from tkinter import filedialog, messagebox
from song_storage import SongStorage

class SavelistWindow:
    def __init__(self, parent, db,user_id):
        self.user_id=user_id
        self.db = db
        self.storage = SongStorage(self.db)
        self.root = Toplevel(parent)
        self.root.title("Creează o Savelist")
        self.root.geometry("400x600")
        self.root.resizable(0, 0)
        self.root.configure(background="plum4")
        self.patrat = Frame(self.root, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat.place(x=20, y=20)
        Label(self.patrat, text="Title:", width=11,font=("Microsoft Yahei UI Light",11,'bold'),background='MistyRose4',foreground='white',bd=2).place(x=20,y=20)
        self.title_var = StringVar()
        Entry(self.patrat, textvariable=self.title_var, font=("Microsoft Yahei UI Light",11,'bold'),width=24,bd=0,highlightthickness=2,
    highlightbackground="LightPink4",
    highlightcolor="LightPink4").place(x=125,y=20)
        Label(self.patrat, text="Artist:", width=11,font=("Microsoft Yahei UI Light",11,'bold'),background='MistyRose4',foreground='white',bd=2).place(x=20,y=60)
        self.artist_var = StringVar()
        Entry(self.patrat, textvariable=self.artist_var, font=("Microsoft Yahei UI Light",11,'bold'),width=24,bd=0,highlightthickness=2,
    highlightbackground="LightPink4",
    highlightcolor="LightPink4").place(x=125,y=60)

        Label(self.patrat, text="Tag:",width=11, font=("Microsoft Yahei UI Light",11,'bold'),background='MistyRose4',foreground='white',bd=2).place(x=20,y=100)
        self.tag_var = StringVar()
        Entry(self.patrat, textvariable=self.tag_var, font=("Microsoft Yahei UI Light",11,'bold'),width=24,bd=0,highlightthickness=2,
    highlightbackground="LightPink4",
    highlightcolor="LightPink4").place(x=125,y=100)

        Label(self.patrat, text="Release Date:", width=11,font=("Microsoft Yahei UI Light",11,'bold'),background='MistyRose4',foreground='white',bd=2).place(x=20,y=140)
        self.release_var = StringVar()
        Entry(self.patrat, textvariable=self.release_var, font=("Microsoft Yahei UI Light",11,'bold'),width=24,bd=0,highlightthickness=2,
    highlightbackground="LightPink4",
    highlightcolor="LightPink4").place(x=125,y=140)

        Button(self.patrat, text="Filtered",bg='LightPink4',fg='white', command=self.filter_songs, font=("Microsoft Yahei UI Light",11,'bold')).place(x=140,y=190)

        self.listbox = Listbox(self.patrat, width=35, font=("Microsoft Yahei UI Light",11,'bold'),bg='LavenderBlush2',selectbackground='PaleVioletRed4')
        self.listbox.place(x=20,y=240)
        scrollbar = Scrollbar(self.patrat, orient='vertical')
        scrollbar.place(x=330, y=240, height=220)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        Button(self.patrat, text="Save The List To A File", bg='LightPink4',fg='white',command=self.save_to_file, font=("Microsoft Yahei UI Light",11,'bold')).place(x=80,y=480)

        self.filtered_songs = []

    def filter_songs(self):
        title = self.title_var.get().lower()
        artist = self.artist_var.get().lower()
        tag = self.tag_var.get().lower()
        release_date = self.release_var.get().lower()

        if not (title or artist or tag or release_date):
            messagebox.showwarning("Căutare invalidă", "Completează cel puțin un câmp pentru a căuta.")
            return  (
        self.listbox.delete(0, END))
        all_songs = self.storage.get_all_songs(self.user_id)
        self.filtered_songs = []
        print(all_songs)


        for song in all_songs:
            song_id, artist_db, title_db, release, tags = song[0], song[3], song[4], song[5], song[6]
            release_str = str(release) if release else ""
            tags_str = tags if isinstance(tags, str) else ""
            tags_list = [t.strip().lower() for t in tags_str.split(',')]
            print(f"Titlu: {title_db}, Artist: {artist_db}, Release: {release_str}, Tags: {tags_str}")  # DEBUG
            match= (
                   (title and title in title_db.lower()) or
               (artist and artist in artist_db.lower()) or
               ( release_date and release_date in release.lower()) or
               (tag and any(tag in t for t in tags_list))
            )
            self.filtered_songs.append(song)
            if match:
                self.listbox.insert(
            END,
            f"{song_id}. {title_db} - {artist_db} | {release_str} | Tags: {tags_str}"
             )

    def save_to_file(self):
        if not self.filtered_songs:
            messagebox.showwarning("Fără rezultate", "Nu există melodii de salvat.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fișier text", "*.txt"), ("CSV", "*.csv")],
            title="Salvează lista ca..."
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for song in self.filtered_songs:
                    line = f"{song[0]},{song[3]},{song[2]},{song[4]},{song[5]}\n"
                    f.write(line)
            messagebox.showinfo("Succes", "Lista a fost salvată cu succes.")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la salvare: {e}")
