from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

class ResetWindow:
    def __init__(self, root, db):
        self.root =Toplevel(root)
        self.db = db
        self.cursor = db.cursor
        self.root.resizable(0,0)
        self.root.title("Reset Page")
        self.root.configure(bg="DarkOrchid4")
        self.root.geometry("400x600")
        self.patrat = Frame(self.root, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat.place(x=20,y=20)
        heading=Label(self.patrat, text="RESET PASSWORD",font=("Microsoft Yahei UI Light",23,'bold'),bg="white",fg="DarkOrchid1")
        heading.place(x=50,y=40)
        self.username_entry = Entry(self.patrat,width=25,font=("Microsoft Yahei UI Light",11,'bold'),bd=0,fg="DarkOrchid1")
        self.username_entry.place(x=45,y=140)
        self.username_entry.insert(0,'Username')
        self.username_entry.bind('<FocusIn>',self.on_enter)



        Frame(self.patrat,width=275,height=2,bg='DarkOrchid1').place(x=45,y=170)

        self.password_entry = Entry(self.patrat, width=25, font=("Microsoft Yahei UI Light", 11, 'bold'), bd=0,
                                    fg="DarkOrchid1")
        self.password_entry.place(x=45, y=220)
        self.password_entry.insert(0, 'New Password')
        self.password_entry.bind('<FocusIn>', self.on_enter_password)

        Frame(self.patrat, width=275, height=2, bg='DarkOrchid1').place(x=45, y=250)
        self.confirm_entry=Entry(self.patrat,width=25,font=("Microsoft Yahei UI Light", 11, 'bold'), bd=0,fg="DarkOrchid1")
        self.confirm_entry.place(x=45, y=300)
        self.confirm_entry.insert(0,"Confirm Password")
        self.confirm_entry.bind('<FocusIn>', self.on_enter_password2)
        Frame(self.patrat, width=275, height=2, bg='DarkOrchid1').place(x=45, y=330)
        self.openeye1=PhotoImage(file="Resurse/red open.png")
        self.eyeButton1=Button(self.patrat,image=self.openeye1,bd=0,bg="white",activebackground='white',cursor='hand2',command=self.hide)

        self.eyeButton1.place(x=290,y=220)
        self.loginButton=Button(self.patrat,text="Submit",font=("Open Sans",16,"bold"),fg="white",bg="DarkOrchid1",activebackground='DarkOrchid1',activeforeground="white",cursor='hand2',bd=0,width=21,command=self.login)
        self.loginButton.place(x=45,y=390)


    def hide(self):
        self.openeye1.config(file="Resurse/close red.png")
        self.password_entry.config(show="*")
        self.confirm_entry.config(show="*")
        self.eyeButton1.config(command=self.show)
    def show(self):
        self.openeye1.config(file="Resurse/red open.png")
        self.password_entry.config(show="")
        self.confirm_entry.config(show="")
        self.eyeButton1.config(command=self.hide)
    def on_enter(self,event):
        if self.username_entry.get() == 'Username':
            self.username_entry.delete(0,END)
    def on_enter_password(self,event):
        if self.password_entry.get() == 'New Password':
            self.password_entry.delete(0,END)

    def on_enter_password2(self,event):
        if self.confirm_entry.get() == 'Confirm Password':
            self.confirm_entry.delete(0,END)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()
        if password != confirm_password:
            messagebox.showerror("Eroare", "Parolele nu se potrivesc.")
            return
        self.cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user = self.cursor.fetchone()
        if user:
            try:
                self.cursor.execute("UPDATE users SET password=%s WHERE username=%s", (password, username))
                self.db.commit()
                messagebox.showinfo("Succes", "Parola a fost resetată.")
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Eroare", f"A apărut o eroare: {e}")
        else:
            messagebox.showerror("Eroare", "Utilizatorul nu există.")