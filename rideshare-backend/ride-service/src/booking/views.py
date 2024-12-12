from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import Booking
from .serializers import BookingSerializer
from ride_matching.models import RideRequest, Driver

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    @action(detail=False, methods=['post'])
    def create_booking(self, request):
        ride_request_id = request.data.get('ride_request_id')
        driver_id = request.data.get('driver_id')
        
        try:
            ride_request = RideRequest.objects.get(id=ride_request_id)
            driver = Driver.objects.get(id=driver_id)
            
            # Create booking with estimated times
            booking = Booking.objects.create(
                ride_request=ride_request,
                driver=driver,
                estimated_pickup_time=datetime.now() + timedelta(minutes=10),
                estimated_dropoff_time=datetime.now() + timedelta(minutes=25),
                fare_amount=ride_request.estimated_fare or Decimal('0')
            )
            
            return Response(BookingSerializer(booking).data)
        except (RideRequest.DoesNotExist, Driver.DoesNotExist):
            return Response(
                {'error': 'Invalid ride request or driver ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def start_ride(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'IN_PROGRESS'
        booking.actual_pickup_time = datetime.now()
        booking.save()
        return Response(BookingSerializer(booking).data)
    
    @action(detail=True, methods=['post'])
    def complete_ride(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'COMPLETED'
        booking.actual_dropoff_time = datetime.now()
        booking.save()
        return Response(BookingSerializer(booking).data)