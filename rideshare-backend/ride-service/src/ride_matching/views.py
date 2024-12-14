from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RideRequest, Driver, Location
from .serializers import RideRequestSerializer, DriverSerializer, LocationSerializer
from .services import RideMatchingService

class RideRequestViewSet(viewsets.ModelViewSet):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer
    ride_service = RideMatchingService()
    
    @action(detail=True, methods=['post'])
    def request_ride(self, request, pk=None):
        ride_request = self.get_object()
        
        nearby_drivers = self.ride_service.find_nearby_drivers(
            ride_request.pickup_location.latitude,
            ride_request.pickup_location.longitude
        )
        
        fare_estimate = self.ride_service.calculate_fare(
            ride_request.pickup_location,
            ride_request.dropoff_location
        )
        
        ride_request.estimated_fare = fare_estimate['total_fare']
        ride_request.status = 'MATCHING'
        ride_request.save()
        
        return Response({
            'available_drivers': DriverSerializer(nearby_drivers, many=True).data,
            'fare_estimate': fare_estimate
        })

    
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    
    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        driver = self.get_object()
        location_serializer = LocationSerializer(data=request.data)
        
        if location_serializer.is_valid():
            location = location_serializer.save()
            driver.current_location = location
            driver.save()
            return Response(DriverSerializer(driver).data)
        return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    