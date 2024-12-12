from decimal import Decimal
from datetime import datetime, timedelta
from .models import Driver, RideRequest, Location
import random

class RideMatchingService:
    def __init__(self):
        self.base_fare = Decimal('5.00')
        self.per_km_rate = Decimal('2.00')
        self.per_minute_rate = Decimal('0.50')
    
    def find_nearby_drivers(self, latitude: Decimal, longitude: Decimal, radius_km: float = 5):
        available_drivers = Driver.objects.filter(is_available=True)
        return list(available_drivers)[:3]
    
    def calculate_fare(self, pickup_location: Location, dropoff_location: Location) -> dict:
        distance_km = 5
        duration_minutes = 15
        
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