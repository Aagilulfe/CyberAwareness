import smtplib, ssl

port = 465  # For SSL
smtp_server="smtp.gmail.com"


sender_email = input("Type your email and press enter: ")
password = input("Type your password and press enter: ")

receiver_email = input("Type the email of the recever and press enter: ")
message = """\
Subject: Challenge4

Ce mail est envoye depuis python."""


#password = input("Type your password and press enter: ")

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)