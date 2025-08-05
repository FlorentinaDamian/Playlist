from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
from requests_oauthlib import OAuth2Session
import webbrowser
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
class LoginWindow:
    def __init__(self, root, db, on_login_success):
        self.root = root
        self.db = db
        self.cursor = db.cursor
        self.on_login_success = on_login_success
        self.root.resizable(0,0)
        self.root.title("Login Page")
        self.root.configure(bg="firebrick4")
        self.root.geometry("400x600")
        self.patrat = Frame(root, width=360, height=560, bg="white", borderwidth=2, relief="solid")
        self.patrat.place(x=20,y=20)
        heading=Label(self.patrat, text="USER LOGIN",font=("Microsoft Yahei UI Light",23,'bold'),bg="white",fg="firebrick1")
        heading.place(x=90,y=40)
        self.username_entry = Entry(self.patrat,width=25,font=("Microsoft Yahei UI Light",11,'bold'),bd=0,fg="firebrick1")
        self.username_entry.place(x=45,y=140)
        self.username_entry.insert(0,'Username')
        self.username_entry.bind('<FocusIn>',self.on_enter)
        Frame(self.patrat,width=275,height=2,bg='firebrick1').place(x=45,y=160)

        self.password_entry = Entry(self.patrat, width=25, font=("Microsoft Yahei UI Light", 11, 'bold'), bd=0,
                                    fg="firebrick1")
        self.password_entry.place(x=45, y=200)
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', self.on_enter_password)
        Frame(self.patrat, width=275, height=2, bg='firebrick1').place(x=45, y=220)
        self.openeye=PhotoImage(file="Resurse/red open.png")
        self.eyeButton=Button(self.patrat,image=self.openeye,bd=0,bg="white",activebackground='white',cursor='hand2',command=self.hide)
        self.eyeButton.place(x=290,y=190)

        self.forgetButton = Button(self.patrat, text='Forgot Password?', bd=0, bg="white", activebackground='white', font=("Microsoft Yahei UI Light", 9, 'bold'),fg="firebrick1",activeforeground="firebrick1",
                                cursor='hand2',command=self.reset)
        self.forgetButton.place(x=200, y=230)

        self.loginButton=Button(self.patrat,text="Login",font=("Open Sans",16,"bold"),fg="white",bg="firebrick1",activebackground='firebrick1',activeforeground="white",cursor='hand2',bd=0,width=21,command=self.login)
        self.loginButton.place(x=45,y=280)
        self.orLabel=Label(self.patrat,text="---------------- OR ----------------",font=("Open Sans",16),fg="firebrick1",bg="white")
        self.orLabel.place(x=47,y=340)
        self.facebook=PhotoImage(file="Resurse/facebook.png")
        self.fbLabel=Button(self.patrat,image=self.facebook,bg="white",command=self.facebook_login)
        self.fbLabel.place(x=80,y=380)

        self.google_login = PhotoImage(file="Resurse/google.png")
        self.fbLabel2 = Button(self.patrat, image=self.google_login, bg="white",command=self.google)
        self.fbLabel2.place(x=150, y=380)

        self.twitter_login = PhotoImage(file="Resurse/twitter.png")
        self.fbLabel3 = Button(self.patrat, image=self.twitter_login, bg="white",command=self.github)
        self.fbLabel3.place(x=220, y=380)

        self.signupLabel=Label(self.patrat,text="Don't have an account?",font=("Open Sans",9,"bold"),fg="firebrick1",bg="white")
        self.signupLabel.place(x=45,y=450)

        self.newaccountButton = Button(self.patrat, text="Create new one", font=("Open Sans", 9, "bold underline"), fg="blue",
                                  bg="white", activebackground='blue', activeforeground="white",
                                  cursor='hand2', bd=0, command=self.signup_page)
        self.newaccountButton.place(x=190, y=450)

    def google(self):
        try:
            scopes=[
                'openid',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'
                ]
            flow =InstalledAppFlow.from_client_secrets_file('Resurse/client_secret.json', scopes=scopes)
            creds=flow.run_local_server(port=8080,prompt='consent')
            headers={'Authorization': f'Bearer {creds.token}'}
            response=requests.get('https://www.googleapis.com/oauth2/v1/userinfo',headers=headers)
            user_info=response.json()
            name=user_info.get('name','unknown')
            email=user_info.get('email','unknown')
            self.cursor.execute("SELECT id FROM users WHERE username=%s", (email,))
            user = self.cursor.fetchone()
            if not user:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (email, 'google_login'))
                self.db.commit()
                user_id = self.cursor.lastrowid
            else:
                user_id = user[0]

            messagebox.showinfo("Login Successful", f"Welcome, {name}!\nYour email is: {email}")
            self.root.destroy()
            self.on_login_success(user_id)
        except Exception as e:
            messagebox.showerror("Login Failed",str(e))

    def facebook_login(self):
        client_id = "client_id"
        client_secret = "client_secret"
        redirect_uri = "http://localhost:8080/callback"

        scope = ['email']
        facebook = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

        authorization_url, state = facebook.authorization_url(
            'https://www.facebook.com/v16.0/dialog/oauth'
        )

        class Handler(BaseHTTPRequestHandler):
            def __init__(inner_self, *args, **kwargs):
                inner_self.outer = self
                inner_self.facebook_session = facebook
                inner_self.client_secret = client_secret
                super().__init__(*args, **kwargs)

            def log_message(self, format, *args):
                pass

            def do_GET(inner_self):
                if inner_self.path.startswith("/callback"):
                    from urllib.parse import urlparse, parse_qs
                    query = parse_qs(urlparse(inner_self.path).query)
                    code = query.get('code', [None])[0]

                    inner_self.send_response(200)
                    inner_self.send_header('Content-type', 'text/html')
                    inner_self.end_headers()
                    inner_self.wfile.write(
                        b"<html><body><h2>Login Facebook reusit! Poti inchide aceasta fereastra.</h2></body></html>")

                    if code:
                        try:
                            token = inner_self.facebook_session.fetch_token(
                                'https://graph.facebook.com/v16.0/oauth/access_token',
                                client_secret=inner_self.client_secret,
                                code=code
                            )
                        except Exception as e:
                            messagebox.showerror("Facebook Login Failed", f"Eroare la token: {e}")
                            return

                        user_info = inner_self.facebook_session.get(
                            'https://graph.facebook.com/me?fields=id,name,email'
                        ).json()

                        name = user_info.get("name", "Facebook User")
                        email = user_info.get("email", None)

                        if email is None:
                            messagebox.showerror("Facebook Login", "Nu am putut obține email-ul.")
                            return

                        inner_self.outer.facebook_login_success(name, email)

        def start_server():
            with HTTPServer(('localhost', 8080), Handler) as httpd:
                httpd.handle_request()

        threading.Thread(target=start_server, daemon=True).start()
        webbrowser.open(authorization_url)

    def facebook_login_success(self, name, email):
        def do_login():
            self.cursor.execute("SELECT id FROM users WHERE username=%s", (email,))
            user = self.cursor.fetchone()
            if not user:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (email, 'facebook_login'))
                self.db.conn.commit()
                user_id = self.cursor.lastrowid
            else:
                user_id = user[0]

            messagebox.showinfo("Facebook Login", f"Welcome, {name}!\nYour email is: {email}")
            self.root.destroy()
            self.on_login_success(user_id)

        self.root.after(0, do_login)

    def reset(self):
        from Reset import ResetWindow
        ResetWindow(self.root,self.db)
    def signup_page(self):
        self.root.destroy()
        from signup import SignupWindow
        SignupWindow(self.db,self.on_login_success)
    def hide(self):
        self.openeye.config(file="Resurse/close red.png")
        self.password_entry.config(show="*")
        self.eyeButton.config(command=self.show)
    def show(self):
        self.openeye.config(file="Resurse/red open.png")
        self.password_entry.config(show="")
        self.eyeButton.config(command=self.hide)
    def on_enter(self,event):
        if self.username_entry.get() == 'Username':
            self.username_entry.delete(0,END)
    def on_enter_password(self,event):
        if self.password_entry.get() == 'Password':
            self.password_entry.delete(0,END)




    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
        user = self.cursor.fetchone()
        if user:
            user_id = user[0]
            messagebox.showinfo("Login reușit", f"Bun venit, {username}!")
            self.root.destroy()
            self.on_login_success(user_id)
        else:
            messagebox.showerror("Eroare", "Username sau parolă greșite.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.db.conn.commit()
            messagebox.showinfo("Cont creat", "Cont creat cu succes. Te poți loga.")
        except:
            messagebox.showerror("Eroare", "Numele de utilizator există deja.")

    def github(self):
        client_id = "cliet_id"
        client_secret = "client_secret"
        redirect_uri = "http://localhost:8080/callback"

        scope = 'read:user,user:email'
        github = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

        authorization_url, state = github.authorization_url('https://github.com/login/oauth/authorize')

        class Handler(BaseHTTPRequestHandler):
            def __init__(inner_self, *args, **kwargs):
                inner_self.outer = self
                inner_self.github_session = github
                inner_self.client_secret = client_secret
                super().__init__(*args, **kwargs)

            def log_message(self, format, *args):
                pass

            def do_GET(inner_self):
                if inner_self.path.startswith("/callback"):
                    from urllib.parse import urlparse, parse_qs
                    query = parse_qs(urlparse(inner_self.path).query)
                    code = query.get('code', [None])[0]

                    inner_self.send_response(200)
                    inner_self.send_header('Content-type', 'text/html')
                    inner_self.end_headers()
                    inner_self.wfile.write(
                        b"<html><body><h2>Login GitHub reusit! Poti inchide aceasta fereastra.</h2></body></html>")

                    if code:
                        try:
                            token = inner_self.github_session.fetch_token(
                                'https://github.com/login/oauth/access_token',
                                client_secret=inner_self.client_secret,
                                code=code,
                            )
                        except Exception as e:
                            messagebox.showerror("GitHub Login Failed", f"Eroare la token: {e}")
                            return

                        user_info = inner_self.github_session.get('https://api.github.com/user').json()
                        email_info = inner_self.github_session.get('https://api.github.com/user/emails').json()

                        name = user_info.get("name", "GitHub User")
                        email = None
                        if isinstance(email_info, list) and len(email_info) > 0:
                            for em in email_info:
                                if em.get('primary') and em.get('verified'):
                                    email = em.get('email')
                                    break
                            if not email:
                                email = email_info[0].get('email')
                        if not email:
                            email = f"{user_info.get('login', 'unknown')}@github.com"

                        inner_self.outer.github_login_success(name, email)

        def start_server():
            with HTTPServer(('localhost', 8080), Handler) as httpd:
                httpd.handle_request()
        threading.Thread(target=start_server, daemon=True).start()
        webbrowser.open(authorization_url)

    def github_login_success(self, name, email):
        def do_login():
            self.cursor.execute("SELECT id FROM users WHERE username=%s", (email,))
            user = self.cursor.fetchone()
            if not user:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (email, 'github_login'))
                self.db.conn.commit()  # folosește corect commit aici
                user_id = self.cursor.lastrowid
            else:
                user_id = user[0]

            messagebox.showinfo("GitHub Login", f"Welcome, {name}!\nYour email is: {email}")
            self.root.destroy()
            self.on_login_success(user_id)

        self.root.after(0, do_login)
