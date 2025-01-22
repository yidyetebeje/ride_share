from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RideRequest, Driver, Location
from .serializers import RideRequestSerializer, DriverSerializer, LocationSerializer
from .services import RideMatchingService

class RideRequestViewSet(viewsets.ModelViewSet):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new ride request"""
        try:
            # Create locations
            pickup_location_data = request.data.get('pickup_location')
            dropoff_location_data = request.data.get('dropoff_location')
            
            pickup_location = Location.objects.create(
                latitude=pickup_location_data['latitude'],
                longitude=pickup_location_data['longitude']
            )
            
            dropoff_location = Location.objects.create(
                latitude=dropoff_location_data['latitude'],
                longitude=dropoff_location_data['longitude']
            )
            
            # Create ride request
            ride_request = RideRequest.objects.create(
                user_id=request.data['user_id'],
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
                status='PENDING'
            )
            
            return Response(
                RideRequestSerializer(ride_request).data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


    @action(detail=True, methods=['post'])
    def request_ride(self, request, pk=None):
        """Request a ride and find nearby drivers"""
        try:
            ride_request = self.get_object()
            ride_service = RideMatchingService()
            
            # Find nearby drivers
            nearby_drivers = ride_service.find_nearby_drivers(
                ride_request.pickup_location.latitude,
                ride_request.pickup_location.longitude
            )
            
            # Calculate fare
            fare_estimate = ride_service.calculate_fare(
                ride_request.pickup_location,
                ride_request.dropoff_location
            )
            
            # Update ride request
            ride_request.estimated_fare = fare_estimate['total_fare']
            ride_request.status = 'MATCHING'
            ride_request.save()
            
            return Response({
                'ride_request': RideRequestSerializer(ride_request).data,
                'nearby_drivers': nearby_drivers,
                'fare_estimate': fare_estimate
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )