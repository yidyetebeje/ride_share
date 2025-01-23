# booking/services.py
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Booking
from ride_matching.models import RideRequest
from ride_matching.services import RideMatchingService
from notification_helper import send_email, send_notification, send_telegram
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DRIVER_SERVICE_URL = "http://driver-service:4343/api/drivers"


class BookingService:
    def __init__(self):
        self.ride_matching_service = RideMatchingService()
        self.default_chat_id = "923913833"
        self.default_email = "yohannesgetachewerieso@gmail.com"

    def get_driver(self, driver_id: int):
        """Fetch driver from driver service"""
        try:
            response = requests.get(f"{DRIVER_SERVICE_URL}/{driver_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch driver: {str(e)}")
            raise

    def create_booking(self, ride_request: RideRequest, driver_id: int) -> Booking:
        """Create a new booking"""
        # Fetch driver from driver service
        driver = self.get_driver(driver_id)
        
        pickup_time = datetime.now() + timedelta(minutes=10)
        duration_minutes = 10
        dropoff_time = pickup_time + timedelta(minutes=duration_minutes)

        booking = Booking.objects.create(
            ride_request=ride_request,
            driver_id=driver_id, 
            estimated_pickup_time=pickup_time,
            estimated_dropoff_time=dropoff_time,
            fare_amount=50.00  
        )
        try:
            message = f"Ride booked! Driver will arrive in {duration_minutes} minutes"
            send_notification(content=message)
            logger.info(f"Notifications sent successfully: {message}")
        except Exception as e:
            logger.error(f"Failed to send notifications: {str(e)}")

        try:
            requests.patch(f"{DRIVER_SERVICE_URL}/{driver_id}/status", 
                         json={"status": "BUSY"})
        except Exception as e:
            print(f"Failed to update driver status: {str(e)}")

        
        return booking

    def accept_ride(self, booking: Booking) -> Booking:
        """Accept a ride"""
        try:
            if booking.status != 'CREATED':
                raise ValueError("Booking must be in CREATED state to accept")

            booking.status = 'ACCEPTED'
            booking.save()

            # Send notifications
            message = f"""Your ride has been accepted! 
            Driver is on the way.
            Estimated pickup time: {booking.estimated_pickup_time.strftime('%I:%M %p')}"""
                    
            send_notification(
                content=message,
                chat_id=self.default_chat_id,
                email=self.default_email
            )

            # Update driver status
            try:
                requests.patch(f"{DRIVER_SERVICE_URL}/{booking.driver_id}/status", 
                            json={"status": "BUSY"})
                logger.info(f"Updated driver {booking.driver_id} status to BUSY")
            except Exception as e:
                logger.error(f"Failed to update driver status: {str(e)}")

            return booking
        except Exception as e:
            logger.error(f"Error accepting ride: {str(e)}")
            raise

    def start_ride(self, booking: Booking) -> Booking:
        """Start a ride"""
        if booking.status != 'CREATED':
            raise ValueError("Booking must be in CREATED state to start")

        booking.status = 'IN_PROGRESS'
        booking.actual_pickup_time = datetime.now()
        booking.save()

        send_notification(content="Your ride has started")

        return booking

    def complete_ride(self, booking: Booking) -> Booking:
        """Complete a ride"""
        if booking.status != 'IN_PROGRESS':
            raise ValueError("Booking must be in IN_PROGRESS state to complete")

        booking.status = 'COMPLETED'
        booking.actual_dropoff_time = datetime.now()
        booking.save()

        send_notification(content=f"Ride completed. Final fare: {booking.fare_amount}")

        # Make driver available again
        booking.driver.is_available = True
        booking.driver.save()

        return booking

    def cancel_ride(self, booking: Booking, reason: str = None) -> Booking:
        """Cancel a ride"""
        if booking.status in ['COMPLETED', 'CANCELLED']:
            raise ValueError("Cannot cancel completed or already cancelled booking")

        booking.status = 'CANCELLED'
        booking.save()

        # Make driver available again
        booking.driver.is_available = True
        booking.driver.save()

        # Update ride request status
        booking.ride_request.status = 'CANCELLED'
        booking.ride_request.save()

        send_notification(content=f"Ride cancelled. {reason if reason else ''}")
        return booking

    def calculate_final_fare(self, booking: Booking) -> Decimal:
        """Calculate final fare based on actual time and distance"""
        if not (booking.actual_pickup_time and booking.actual_dropoff_time):
            return booking.fare_amount

        # Get actual duration
        duration = booking.actual_dropoff_time - booking.actual_pickup_time
        actual_minutes = duration.total_seconds() / 60

        # Recalculate fare with actual duration
        fare_estimate = self.ride_matching_service.calculate_fare(
            booking.ride_request.pickup_location,
            booking.ride_request.dropoff_location
        )
        
        return fare_estimate['total_fare']
    
    