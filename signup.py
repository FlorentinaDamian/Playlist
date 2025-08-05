from tkinter import *
from tkinter import messagebox
import bcrypt
import re
from email_send import FereastraVerificare
from email_send import trimite_email_verificare
class SignupWindow:
    def __init__(self, db,on_login_success):
        self.db = db
        self.on_login_success = on_login_success
        self.cursor = db.cursor
        self.signup_window = Tk()
        self.signup_window.title("SignUp Page")
        self.signup_window.geometry("400x600")
        self.signup_window.resizable(0, 0)
        self.signup_window.configure(bg="firebrick4")
        self.patrat2 = Frame(self.signup_window, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat2.place(x=20, y=20)
        heading = Label(self.patrat2, text="CREATE AN ACCOUNT", font=("Microsoft Yahei UI Light", 18, 'bold'),
                        bg="white",
                        fg="firebrick1")
        heading.place(x=50, y=30)
        self.emailLabel = Label(self.patrat2, text="Email", font=("Microsoft Yahei UI Light", 10, 'bold'), bg="white",
                                fg="firebrick1")
        self.emailLabel.place(x=50, y=110)
        self.emailEntry = Entry(self.patrat2, width=30, font=("Microsoft Yahei UI Light", 10, 'bold'), fg="white",
                                bg="firebrick1")
        self.emailEntry.place(x=50, y=140)

        self.usernameLabel = Label(self.patrat2, text="Username", font=("Microsoft Yahei UI Light", 10, 'bold'),
                                   bg="white",
                                   fg="firebrick1")
        self.usernameLabel.place(x=50, y=180)
        self.usernameEntry = Entry(self.patrat2, width=30, font=("Microsoft Yahei UI Light", 10, 'bold'), fg="white",
                                   bg="firebrick1")
        self.usernameEntry.place(x=50, y=210)

        self.passwordLabel = Label(self.patrat2, text="Password", font=("Microsoft Yahei UI Light", 10, 'bold'),
                                   bg="white",
                                   fg="firebrick1")
        self.passwordLabel.place(x=50, y=250)
        self.passwordEntry = Entry(self.patrat2, width=30, font=("Microsoft Yahei UI Light", 10, 'bold'), fg="white",
                                   bg="firebrick1")
        self.passwordEntry.place(x=50, y=280)

        self.confirmLabel = Label(self.patrat2, text="Confirm Password", font=("Microsoft Yahei UI Light", 10, 'bold'),
                                  bg="white",
                                  fg="firebrick1")
        self.confirmLabel.place(x=50, y=330)
        self.confirmEntry = Entry(self.patrat2, width=30, font=("Microsoft Yahei UI Light", 10, 'bold'), fg="white",
                                  bg="firebrick1")
        self.confirmEntry.place(x=50, y=360)
        self.agree_var = IntVar()
        self.termscondition = Checkbutton(self.patrat2, text="I agree to the Terms & Conditions",
                                          font=("Microsoft Yahei UI Light", 9, 'bold'), bg="white", fg="firebrick1",
                                          activebackground='white', activeforeground="firebrick1", cursor="hand2", variable=self.agree_var)
        self.termscondition.place(x=45, y=400)

        self.SignupButton = Button(self.patrat2, text="SignUp", font=("Open Sans", 16, "bold"), bd=0, bg="firebrick1",
                                   fg="white", activebackground='firebrick1', activeforeground="white", width=19,command=self.connect_database)
        self.SignupButton.place(x=50, y=480)
        self.sigLabel = Label(self.patrat2, text="Have an account?", font=("Open Sans", 9, "bold"),
                              fg="firebrick1", bg="white")
        self.sigLabel.place(x=45, y=430)

        self.newButton = Button(self.patrat2, text="Log in", font=("Open Sans", 9, "bold underline"),
                                fg="blue",
                                bg="white", activebackground='blue', activeforeground="white",
                                cursor='hand2', bd=0, command=self.login_page)
        self.newButton.place(x=150, y=430)
        self.signup_window.mainloop()
    def login_page(self):
        self.signup_window.destroy()
        from login import LoginWindow
        self.root=Tk()
        LoginWindow(self.root,self.db, self.on_login_success)
        self.root.mainloop()

    def connect_database(self):
        email = self.emailEntry.get().strip()
        username = self.usernameEntry.get().strip()
        password = self.passwordEntry.get().strip()
        confirm = self.confirmEntry.get().strip()

        if not email or not username or not password:
            messagebox.showerror("Error", "All Fields Are Required")
        elif password != confirm:
            messagebox.showerror("Error", "Passwords Do Not Match")
        elif self.agree_var.get() == 0:
            messagebox.showerror("Error", "Please Accept Terms & Conditions")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid Email Address")
        else:
            self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = self.cursor.fetchone()
            if row is not None:
                messagebox.showerror("Error", "Username Already Exists")
                return

            cod = trimite_email_verificare(email)
            if not cod:
                messagebox.showerror("Error", "Nu s-a putut trimite emailul.")
                return

            def creeaza_cont_dupa_verificare():
                try:
                    self.cursor.execute(
                        "INSERT INTO users(username,password,email) VALUES(%s,%s,%s)",
                        (username, password, email)
                    )
                    self.db.commit()
                    messagebox.showinfo("Success", "Cont creat cu succes!")
                    self.clear()
                    self.signup_window.destroy()
                    from login import LoginWindow
                    self.root = Tk()
                    LoginWindow(self.root, self.db, self.on_login_success)
                except Exception as e:
                    messagebox.showerror("Error", f"Database Error: {e}")

            FereastraVerificare(self.signup_window, cod, creeaza_cont_dupa_verificare)

    def clear(self):
        self.passwordEntry.delete(0, END)
        self.confirmEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        self.usernameEntry.delete(0, END)
        self.agree_var.set(0)
