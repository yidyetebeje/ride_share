from rest_framework import serializers
from .models import Booking
from ride_matching.serializers import RideRequestSerializer, DriverSerializer

class BookingSerializer(serializers.ModelSerializer):
    ride_request = RideRequestSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'ride_request', 'driver', 'status', 
                 'estimated_pickup_time', 'estimated_dropoff_time',
                 'actual_pickup_time', 'actual_dropoff_time',
                 'fare_amount', 'created_at', 'updated_at']