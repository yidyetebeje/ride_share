from typing import Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# Hardcoded SMTP and Telegram credentials
SMTP_USER = "yohannesgetachew.e@gmail.com"
SMTP_PASS = "bjlf npye ljfj zehy"
TELEGRAM_BOT_TOKEN = "8042429948:AAGbdGpsvVJQPjdtDbb5dLqeVA6ULym5QKI"

# Function to send email
def send_email(to:str = "ruthwossen75@gmail.com", content:str = "Ride Update"):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"Ride Sharing App <{SMTP_USER}>"
        msg['To'] = to
        msg['Subject'] = "🚗 Ride Sharing Notification"

        body = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4; border-radius: 5px;">
          <h2 style="color: #333;">Hello!</h2>
          <p style="color: #555;">{content}</p>
          <p style="color: #555;">Thank you for using our service!</p>
          <footer style="margin-top: 20px; font-size: 12px; color: #888;">
            &copy; {datetime.now().year} Ride Sharing App. All rights reserved.
          </footer>
        </div>
        """
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to, msg.as_string())
        server.quit()

        print(f"Email sent to {to}")
    except Exception as e:
        print("Error sending email:", e)
        raise

# Function to send Telegram message
def send_telegram(chat_id:str = "923913833", content:str = "Ride Update"):
    try:
        message = f"""
        *🚗 Ride Sharing Notification*

        _Hello!_

        {content}

        Thank you for choosing our service! 🚀

        If you have any questions, feel free to reach out to us.
        """

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': "Markdown"
        }
        logger.info(f"Sending Telegram message to {chat_id}")
        logger.info(f"Payload: {payload}")

        response = requests.post(url, json=payload)
        response.raise_for_status()

        print(f"Message sent to chat ID {chat_id}")
    except Exception as e:
        print("Error sending Telegram message:", e)
        raise

def send_notification(content: str, chat_id: str = "923913833", email: str = "yohannesgetachewerieso@gmail.com"):
    """Send both Telegram and Email notifications"""
    try:
        send_telegram(chat_id=chat_id, content=content)
        send_email(to=email, content=content)
        logger.info("All notifications sent successfully")
        return True
    except Exception as e:
        logger.error(f"Error in send_notification: {str(e)}")
        raise