from rest_framework import serializers
from .models import Booking
from ride_matching.serializers import RideRequestSerializer

class BookingSerializer(serializers.ModelSerializer):
    ride_request = RideRequestSerializer(read_only=True)
    driver_id = serializers.IntegerField()
    
    class Meta:
        model = Booking
        fields = ['id', 'ride_request', 'ride_request_id', 'driver_id', 'status',
                 'estimated_pickup_time', 'estimated_dropoff_time',
                 'actual_pickup_time', 'actual_dropoff_time',
                 'fare_amount', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'estimated_pickup_time': {'required': False},
            'estimated_dropoff_time': {'required': False},
            'fare_amount': {'required': False}
        }

