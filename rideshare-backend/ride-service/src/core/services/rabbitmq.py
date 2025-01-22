import pika
import json
import logging
from django.conf import settings
from functools import wraps
import time

logger = logging.getLogger(__name__)

def with_retry(max_retries=5, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except pika.exceptions.AMQPConnectionError as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"RabbitMQ connection attempt {attempt + 1} failed. Retrying...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class RabbitMQService:
    def __init__(self):
        self.connection = None
        self.channel = None

    @with_retry()
    def connect(self):
        # Use rabbitmq hostname when in Docker, localhost otherwise
        host = 'rabbitmq' if settings.IN_DOCKER else 'localhost'
        port = 5673
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port)
        )
        self.channel = self.connection.channel()
        
        # Declare queues
        self.channel.queue_declare(queue='driver_updates', durable=True)
        self.channel.queue_declare(queue='ride_requests', durable=True)
        
        logger.info("Connected to RabbitMQ")

    def publish_ride_request(self, ride_request):
        if not self.channel:
            self.connect()
            
        message = {
            'ride_request_id': ride_request.id,
            'pickup_location': {
                'latitude': float(ride_request.pickup_location.latitude),
                'longitude': float(ride_request.pickup_location.longitude)
            },
            'dropoff_location': {
                'latitude': float(ride_request.dropoff_location.latitude),
                'longitude': float(ride_request.dropoff_location.longitude)
            },
            'timestamp': ride_request.created_at.isoformat()
        }
        
        self.channel.basic_publish(
            exchange='',
            routing_key='ride_requests',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            )
        )

    def start_consuming_driver_updates(self, callback):
        if not self.channel:
            self.connect()
            
        def wrapped_callback(ch, method, properties, body):
            try:
                data = json.loads(body)
                callback(data)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue='driver_updates',
            on_message_callback=wrapped_callback
        )
        
        logger.info("Started consuming driver updates")
        self.channel.start_consuming()

rabbitmq_service = RabbitMQService()