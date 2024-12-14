from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Booking
from .serializers import BookingSerializer
from ride_matching.models import RideRequest, Driver

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request):
        """Get all bookings"""
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create a booking"""
        try:
            ride_request = RideRequest.objects.get(
                id=request.data.get('ride_request_id')
            )
            driver = Driver.objects.get(
                id=request.data.get('driver_id')
            )
            
            # Create booking
            booking = Booking.objects.create(
                ride_request=ride_request,
                driver=driver,
                estimated_pickup_time=datetime.now() + timedelta(minutes=10),
                estimated_dropoff_time=datetime.now() + timedelta(minutes=25),
                fare_amount=ride_request.estimated_fare or Decimal('0')
            )
            
            # Update ride request and driver status
            ride_request.status = 'MATCHED'
            ride_request.save()
            
            driver.is_available = False
            driver.save()
            
            return Response(BookingSerializer(booking).data)
            
        except (RideRequest.DoesNotExist, Driver.DoesNotExist) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def start_ride(self, request, pk=None):
        try:
            booking = self.get_object()
            booking.status = 'IN_PROGRESS'
            booking.actual_pickup_time = datetime.now()
            booking.save()
            return Response(BookingSerializer(booking).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def complete_ride(self, request, pk=None):
        try:
            booking = self.get_object()
            booking.status = 'COMPLETED'
            booking.actual_dropoff_time = datetime.now()
            booking.save()
            
            # Make driver available again
            booking.driver.is_available = True
            booking.driver.save()
            
            return Response(BookingSerializer(booking).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def cancel_ride(self, request, pk=None):
        try:
            booking = self.get_object()
            booking.status = 'CANCELLED'
            booking.save()
            
            # Make driver available again
            booking.driver.is_available = True
            booking.driver.save()
            
            return Response(BookingSerializer(booking).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )