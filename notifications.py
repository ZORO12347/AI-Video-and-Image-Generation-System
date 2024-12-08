import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("EMAIL_PASSWORD")

    def send_email(self, recipient, subject, body):
        """Send an email notification."""
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = recipient
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.sendmail(self.email, recipient, msg.as_string())
        except Exception as e:
            print(f"Error sending email: {e}")
