from django.db import models
from ride_matching.models import RideRequest, Driver

class Booking(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('ACCEPTED', 'Accepted'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    ride_request_id = models.IntegerField(default=0)
    driver_id = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='CREATED'
    )
    estimated_pickup_time = models.DateTimeField()
    estimated_dropoff_time = models.DateTimeField()
    actual_pickup_time = models.DateTimeField(null=True, blank=True)
    actual_dropoff_time = models.DateTimeField(null=True, blank=True)
    fare_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'