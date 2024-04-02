import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject: str, body: str):
    host = 'smtp.gmail.com'
    port = '587'
    user = 'alexing10@gmail.com'
    password = os.getenv('EMAIL_HOST_PASSWORD')
    recipient = user

    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server = smtplib.SMTP(host, port)
    server.starttls()  # Secure the connection
    server.login(user, password)
    text = msg.as_string()
    server.sendmail(user, recipient, text)
    server.quit()

    print("Email sent successfully!")
