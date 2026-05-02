from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os, smtplib, ssl

load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('APP_PASSWORD')

def send_email(to, subject, message):
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(email, password)
        
            msg = MIMEMultipart('alternative')
            msg['To'] = to
            msg['Subject'] = subject
            msg['From'] = email
            msg.attach(MIMEText(message, 'plain'))

            server.sendmail(email, to, msg.as_string())
            print('Email sent successfully!')
    except(smtplib.SMTPAuthenticationError, smtplib.SMTPConnectError, smtplib.SMTPRecipientsRefused) as e:
        print('Something went wrong: ', e)
        return

def main():
    to = input('Receipient: ')
    subject = input('Subject: ')
    message = input('Message: ')

    if to == '':
        print('No receipient specified')
    elif '@' not in to or '.' not in to:
        print('Invalid email address')
    else:
        send_email(to, subject, message)

main()