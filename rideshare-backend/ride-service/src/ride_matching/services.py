from decimal import Decimal
from datetime import datetime, timedelta
import random
from .models import Driver, Location


class RideMatchingService:
    def __init__(self):
        self.base_fare = Decimal('5.00')
        self.per_km_rate = Decimal('2.00')
        self.per_minute_rate = Decimal('0.50')

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Mock distance calculation"""
        # Simple mock distance (in real world, use haversine formula)
        return random.uniform(1, 10)

    def find_nearby_drivers(self, latitude, longitude, radius_km=5):
        """Find available drivers within radius"""
        available_drivers = Driver.objects.filter(is_available=True)
        
        nearby_drivers = []
        for driver in available_drivers:
            if driver.current_location:
                distance = self.calculate_distance(
                    latitude, longitude,
                    driver.current_location.latitude,
                    driver.current_location.longitude
                )
                if distance <= radius_km:
                    nearby_drivers.append(driver)
        
        return nearby_drivers[:3]  # Return max 3 drivers

    def calculate_fare(self, pickup_location, dropoff_location):
        """Calculate ride fare"""
        distance_km = self.calculate_distance(
            pickup_location.latitude,
            pickup_location.longitude,
            dropoff_location.latitude,
            dropoff_location.longitude
        )
        
        # Mock duration based on distance
        duration_minutes = int(distance_km * 3)  

        
        distance_fare = self.per_km_rate * Decimal(str(distance_km))
        time_fare = self.per_minute_rate * Decimal(str(duration_minutes))
        total_fare = self.base_fare + distance_fare + time_fare
        
        return {
            'base_fare': self.base_fare,
            'distance_fare': distance_fare,
            'time_fare': time_fare,
            'total_fare': total_fare,
            'distance_km': distance_km,
            'duration_minutes': duration_minutes
        }