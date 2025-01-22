from django.db import models
from decimal import Decimal
import math

class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def distance_to(self, other_location):
        """Calculate distance to another location in kilometers"""
        R = 6371  # Earth's radius in km
        lat1 = float(self.latitude)
        lon1 = float(self.longitude)
        lat2 = float(other_location.latitude)
        lon2 = float(other_location.longitude)
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2) * math.sin(dlon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('MATCHING', 'Matching'),
        ('MATCHED', 'Matched'),
        ('CANCELLED', 'Cancelled')
    ]
    
    user_id = models.CharField(max_length=100)
    pickup_location = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE,
        related_name='pickup_requests'
    )
    dropoff_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='dropoff_requests'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    matched_driver_id = models.IntegerField(null=True, blank=True)
    estimated_fare = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    max_matching_radius = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5.0  # 5 km radius
    )