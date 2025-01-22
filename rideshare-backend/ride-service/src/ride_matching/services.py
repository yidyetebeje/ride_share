import requests
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class RideMatchingService:
    def __init__(self):
        self.driver_service_url = "http://driver-service:4343/api"

    def find_nearby_drivers(self, latitude, longitude, radius_km=5):
        """Find nearby available drivers"""
        try:
            response = requests.get(
                f"{self.driver_service_url}/drivers/nearby/",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "radius": radius_km
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error finding nearby drivers: {str(e)}")
            return []

    def calculate_fare(self, pickup_location, dropoff_location):
        """Calculate estimated fare for the ride"""
        # Basic fare calculation
        base_fare = Decimal('5.00')
        per_km_rate = Decimal('2.00')
        
        # Calculate distance
        distance = pickup_location.distance_to(dropoff_location)
        
        # Calculate fare
        distance_fare = Decimal(str(distance)) * per_km_rate
        total_fare = base_fare + distance_fare
        
        return {
            'base_fare': float(base_fare),
            'distance_fare': float(distance_fare),
            'total_fare': float(total_fare),
            'distance_km': float(distance)
        }