import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "you@example.com"
    msg['To'] = to_email

    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)
