from django.db import models
from decimal import Decimal

class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"

class Driver(models.Model):
    driver_id = models.CharField(max_length=100)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)

    def __str__(self):
        return f"Driver {self.driver_id}"

class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('MATCHING', 'Matching'),
        ('MATCHED', 'Matched'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user_id = models.CharField(max_length=100)
    pickup_location = models.ForeignKey(
        Location, related_name='pickup_requests',
        on_delete=models.CASCADE
    )
    dropoff_location = models.ForeignKey(
        Location, related_name='dropoff_requests',
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"