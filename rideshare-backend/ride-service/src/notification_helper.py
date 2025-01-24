from typing import Optional
import smtplib # We will remove these direct email and telegram dependencies here
from email.mime.multipart import MIMEMultipart # ...
from email.mime.text import MIMEText # ...
import requests # ...
from datetime import datetime
import logging
import pika  # Import pika for RabbitMQ
import json # For serializing data to send to RabbitMQ

logger = logging.getLogger(__name__)

# Hardcoded SMTP and Telegram credentials (These should ideally be environment variables)
SMTP_USER = "yohannesgetachew.e@gmail.com"
SMTP_PASS = "bjlf npye ljfj zehy"
TELEGRAM_BOT_TOKEN = "8042429948:AAGbdGpsvVJQPjdtDbb5dLqeVA6ULym5QKI"

# RabbitMQ Connection Parameters (Adjust as needed for your setup)
RABBITMQ_HOST = 'rabbitmq'  # If RabbitMQ is in Docker, use the Docker service name if they are in the same network
RABBITMQ_QUEUE_NAME = 'notification_queue' # Name of the queue for notifications

def publish_message_rabbitmq(queue_name: str, message: dict):
    """Publishes a message to RabbitMQ."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True) # Ensure queue exists and is durable (messages persist)

        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=json.dumps(message), # Serialize message to JSON
                              properties=pika.BasicProperties(
                                  delivery_mode=2, # make message persistent
                              ))
        print(f" [x] Sent message to queue '{queue_name}': {message}")
        connection.close()
    except Exception as e:
        print(f"Error publishing to RabbitMQ: {e}")
        raise

def send_notification(content: str, chat_id: str = "923913833", email: str = "yohannesgetachewerieso@gmail.com"):
    """Sends notification data to RabbitMQ for processing by the notification service."""
    try:
        notification_data = {
            "type": "notification", # You can add a type if you have different kinds of messages
            "email": email,
            "telegram_chat_id": chat_id,
            "content": content
        }
        publish_message_rabbitmq(RABBITMQ_QUEUE_NAME, notification_data)
        logger.info("Notification message published to RabbitMQ")
        return True
    except Exception as e:
        logger.error(f"Error in send_notification: {str(e)}")
        raise

