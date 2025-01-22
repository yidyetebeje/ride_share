from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
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
        """Create a new booking"""
        try:

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error creating booking: {str(e)}") 
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR

            )
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a booking by a driver"""
        try:
            booking = self.get_object()
            
            if booking.status != 'CREATED':
                return Response(
                    {'error': 'Only CREATED bookings can be accepted'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            booking.status = 'ACCEPTED'
            booking.save()
            
            # Optional: Notify user through RabbitMQ that driver accepted
            # self.notify_user(booking)
            
            return Response(self.get_serializer(booking).data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def start_ride(self, request, pk=None):
        """Start the ride"""
        try:
            booking = self.get_object()
            if booking.status != 'ACCEPTED':
                return Response(
                    {'error': 'Ride must be accepted before starting'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            booking.status = 'IN_PROGRESS'
            booking.actual_pickup_time = datetime.now()
            booking.save()
            return Response(self.get_serializer(booking).data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def complete_ride(self, request, pk=None):
        """Complete the ride"""
        booking = self.get_object()
        if booking.status != 'IN_PROGRESS':
            return Response(
                {'error': 'Ride must be in progress before completing'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'COMPLETED'
        booking.actual_dropoff_time = datetime.now()
        booking.save()
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=['post'])
    def cancel_ride(self, request, pk=None):
        """Cancel the ride"""
        booking = self.get_object()
        if booking.status in ['COMPLETED', 'CANCELLED']:
            return Response(
                {'error': 'Cannot cancel completed or already cancelled ride'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'CANCELLED'
        booking.save()
        return Response(self.get_serializer(booking).data)

