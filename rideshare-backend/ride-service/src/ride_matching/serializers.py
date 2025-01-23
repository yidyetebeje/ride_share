from rest_framework import serializers
from .models import Location, RideRequest

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'latitude', 'longitude']


class RideRequestSerializer(serializers.ModelSerializer):
    pickup_location = LocationSerializer()
    dropoff_location = LocationSerializer()
    
    class Meta:
        model = RideRequest
        fields = ['id', 'user_id', 'pickup_location', 'dropoff_location', 
                 'status', 'created_at', 'estimated_fare']
    
    def create(self, validated_data):
        pickup_location_data = validated_data.pop('pickup_location')
        dropoff_location_data = validated_data.pop('dropoff_location')
        
        pickup_location = Location.objects.create(**pickup_location_data)
        dropoff_location = Location.objects.create(**dropoff_location_data)
        
        return RideRequest.objects.create(
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            **validated_data
        )