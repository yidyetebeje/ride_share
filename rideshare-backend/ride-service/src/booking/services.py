# booking/services.py
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Booking
from ride_matching.models import RideRequest, Driver
from ride_matching.services import RideMatchingService

class BookingService:
    def __init__(self):
        self.ride_matching_service = RideMatchingService()

    def create_booking(self, ride_request: RideRequest, driver: Driver) -> Booking:
        """Create a new booking"""
        # Calculate estimated times
        pickup_time = datetime.now() + timedelta(minutes=10)
        
        # Get distance and duration from ride matching service
        fare_estimate = self.ride_matching_service.calculate_fare(
            ride_request.pickup_location,
            ride_request.dropoff_location
        )
        
        duration_minutes = fare_estimate['duration_minutes']
        dropoff_time = pickup_time + timedelta(minutes=duration_minutes)

        # Create booking
        booking = Booking.objects.create(
            ride_request=ride_request,
            driver=driver,
            estimated_pickup_time=pickup_time,
            estimated_dropoff_time=dropoff_time,
            fare_amount=fare_estimate['total_fare']
        )

        # Update ride request status
        ride_request.status = 'MATCHED'
        ride_request.save()

        # Update driver availability
        driver.is_available = False
        driver.save()

        return booking

    def start_ride(self, booking: Booking) -> Booking:
        """Start a ride"""
        if booking.status != 'CREATED':
            raise ValueError("Booking must be in CREATED state to start")

        booking.status = 'IN_PROGRESS'
        booking.actual_pickup_time = datetime.now()
        booking.save()

        return booking

    def complete_ride(self, booking: Booking) -> Booking:
        """Complete a ride"""
        if booking.status != 'IN_PROGRESS':
            raise ValueError("Booking must be in IN_PROGRESS state to complete")

        booking.status = 'COMPLETED'
        booking.actual_dropoff_time = datetime.now()
        booking.save()

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
    
    