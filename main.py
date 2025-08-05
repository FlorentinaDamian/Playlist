from tkinter import Tk
from Database import Database
from login import LoginWindow
from meniu import meniu

def main():
    root = Tk()
    db = Database()
    def start_main_menu(user_id):
        meniu_root = Tk()
        meniu(meniu_root, db, user_id)
        meniu_root.mainloop()
    LoginWindow(root, db, start_main_menu)
    root.mainloop()
if __name__ == "__main__":
    main()
