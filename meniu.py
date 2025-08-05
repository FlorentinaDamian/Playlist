from tkinter import *
from Database import Database
from grafica import SongApp
from delete import SongListView
from modificare import EditSongsWindow
from search import SearchWindow
from savelist import SavelistWindow
from play import PlayWindow
class meniu:
    def __init__(self, root, db,user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("meniu")
        self.root.geometry("400x600")
        self.root.resizable(0, 0)
        self.root.configure(bg="dark slate blue")
        self.patrat = Frame(self.root, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat.place(x=20, y=20)
        self.db=db
        heading = Label(self.patrat, text="MENU", font=("Microsoft Yahei UI Light", 23, 'bold'), bg="white",
                        fg="light slate blue")
        heading.place(x=130, y=40)


        self.button_add=Button(self.patrat,width=28,font=("Microsoft Yahei UI Light",12,'bold'),text="Add Song",command=self.add_song,bg='medium purple',fg='white',height=2,activeforeground='white',activebackground='medium slate blue')
        self.button_add.place(x=35,y=120)

        self.button_delete = Button(self.patrat, text="Delete Song", font=("Microsoft Yahei UI Light",12,'bold'), command=self.delete_song,width=28,bg='medium purple',fg='white',height=2,activeforeground='white',activebackground='medium slate blue')
        self.button_delete.place(x=35,y=190)

        self.button_modificare = Button(self.patrat, text="Change Metadata", font=("Microsoft Yahei UI Light",12,'bold'), command=lambda: EditSongsWindow(root, self.db,self.user_id),width=28,bg='medium purple',fg='white',height=2,activeforeground='white',activebackground='medium slate blue')
        self.button_modificare.place(x=35,y=260)
        self.button_creare = Button(self.patrat, text="Create Savelist", font=("Microsoft Yahei UI Light",12,'bold'), command=self.create_song,width=28,bg='medium purple',fg='white',height=2,activeforeground='white',activebackground='medium slate blue')
        self.button_creare.place(x=35,y=330)
        self.button_search = Button(self.patrat, text="Search", font=("Microsoft Yahei UI Light",12,'bold'), command=self.search_song,width=28,bg='medium purple',fg='white',height=2,activeforeground='white',activebackground='medium slate blue')
        self.button_search.place(x=35,y=400)
        self.button_play = Button(self.patrat, text="Play", font=("Microsoft Yahei UI Light",12,'bold'), command=self.play_song,width=28,bg='medium purple',fg='white',height=2,activeforeground='white',activebackground='medium slate blue')
        self.button_play.place(x=35,y=470)
    def add_song(self):
        root = Tk()
        app = SongApp(root, self.db, self.user_id)
        root.mainloop()
    def delete_song(self):
        root = Tk()
        app = SongListView(root,self.db,self.user_id)
        root.mainloop()
    def modify_song(self):
        root =Tk()
        app = EditSongsWindow(root,self.db,self.user_id)
        root.mainloop()
    def search_song(self):
        #root = Tk()
        app = SearchWindow(self.root, self.db,self.user_id)
        self.root.mainloop()
    def play_song(self):
        root = Tk()
        app=PlayWindow(root,self.db,self.user_id)
        root.mainloop()
    def create_song(self):
        app = SavelistWindow(self.root, self.db,self.user_id)
        self.root.mainloop()
