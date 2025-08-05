import smtplib
import random
from email.message import EmailMessage
from tkinter import *
def trimite_email_verificare(destinatar):
    cod = str(random.randint(100000, 999999))
    email = EmailMessage()
    email['From'] = "adresa88@gmail.com"
    email['To'] = destinatar
    email['Subject'] = "Cod de verificare cont"
    email.set_content(f"Codul tău de verificare este: {cod}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            smtp.login('adresa@gmail.com', 'password')
            smtp.send_message(email)
        return cod
    except Exception as e:
        print("Eroare trimitere email:", e)
        return None

class FereastraVerificare:
    def __init__(self, parent, cod_corect, callback_confirmare):
        self.cod_corect = cod_corect
        self.callback_confirmare = callback_confirmare

        self.root = Toplevel(parent)
        self.root.title("Verificare Email")
        self.root.geometry("300x180")
        self.root.configure(bg="wheat")

        Label(self.root, text="Introdu codul primit pe email:", bg="wheat").pack(pady=10)
        self.cod_entry = Entry(self.root, font=("Arial", 14), justify='center')
        self.cod_entry.pack()

        Button(self.root, text="Verifică", command=self.verifica_cod,
               bg="firebrick3", fg="white").pack(pady=15)

    def verifica_cod(self):
        if self.cod_entry.get().strip() == self.cod_corect:
            self.root.destroy()
            self.callback_confirmare()
        else:
            self.cod_entry.delete(0, END)
            self.cod_entry.insert(0, "Cod greșit")
