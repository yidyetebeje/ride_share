from django.db import models
from ride_matching.models import RideRequest  


class Booking(models.Model):
    ride_request = models.ForeignKey(RideRequest, on_delete=models.CASCADE, null=True)
    driver_id = models.IntegerField() 
    status = models.CharField(max_length=20, default='CREATED')
    estimated_pickup_time = models.DateTimeField()
    estimated_dropoff_time = models.DateTimeField()
    actual_pickup_time = models.DateTimeField(null=True)
    actual_dropoff_time = models.DateTimeField(null=True)
    fare_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'

        