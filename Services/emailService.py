import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, recipient_email, body_html):
    email_sender = os.getenv('GoogleMail__EmailSender')
    email_password = os.getenv('GoogleMail__ApiKey')
    smtp_server = os.getenv('GoogleMail__Host')
    smtp_port = os.getenv('GoogleMail__Port')

    print(f'Email sender: {email_sender}')
    print(f'Email password: {email_password}')
    print(f'SMTP server: {smtp_server}')
    print(f'SMTP port: {smtp_port}')

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html'))

    try:
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient_email, msg.as_string())
        return True
    except Exception as e:
        return False, str(e)
