from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from decimal import Decimal
from .models import Booking
from .serializers import BookingSerializer
from ride_matching.models import RideRequest
from notification_helper import send_notification
from .services import BookingService
import logging

logger = logging.getLogger(__name__)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.booking_service = BookingService() 

    def create(self, request):
        """Create a new booking"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                booking = serializer.save()
                message = f"Ride booked! Driver will arrive in 10 minutes"
                try:
                    send_notification(
                        content=message,
                        chat_id=self.booking_service.default_chat_id,
                        email=self.booking_service.default_email
                    )
                
                    logger.info("Notifications sent successfully")
                except Exception as e:
                    logger.error(f"Failed to send notifications: {str(e)}")
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating booking: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=True, methods=['post'])
    def accept_ride(self, request, pk=None):
        """Accept a ride booking"""
        try:
            booking = self.get_object()
            
            if booking.status != 'CREATED':
                return Response(
                    {'error': 'Booking must be in CREATED state to accept'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update booking status
            booking.status = 'ACCEPTED'
            booking.save()

            # Send notifications
            message = "Your ride has been accepted! Driver is on the way. Estimated pickup time: 5mins"
            try:
                send_notification(
                        content=message,
                        chat_id=self.booking_service.default_chat_id,
                        email=self.booking_service.default_email
                    )
                logger.info("Notifications sent successfully")
            except Exception as e:
                logger.error(f"Failed to send notifications: {str(e)}")
            
            return Response(
                self.get_serializer(booking).data,
                status=status.HTTP_200_OK
            )
            
        except ValueError as e:
            logger.error(f"Validation error in accept_ride: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error accepting ride: {str(e)}")
            return Response(
                {'error': 'Failed to accept ride'},
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

            # Send notifications
            message = "Your ride has started"
            try:
                send_notification(
                        content=message,
                        chat_id=self.booking_service.default_chat_id,
                        email=self.booking_service.default_email
                    )
            except Exception as e:
                logger.error(f"Failed to send notifications: {str(e)}")

            return Response(self.get_serializer(booking).data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def complete_ride(self, request, pk=None):
        """Complete the ride"""
        try:
            booking = self.get_object()
            if booking.status != 'IN_PROGRESS':
                return Response(
                    {'error': 'Ride must be in progress before completing'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            booking.status = 'COMPLETED'
            booking.actual_dropoff_time = datetime.now()
            booking.save()

            # Send notifications
            message = f"Ride completed. Final fare: ${booking.fare_amount}"
            try:
                 send_notification(
                        content=message,
                        chat_id=self.booking_service.default_chat_id,
                        email=self.booking_service.default_email
                    )
            except Exception as e:
                logger.error(f"Failed to send notifications: {str(e)}")

            return Response(self.get_serializer(booking).data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def cancel_ride(self, request, pk=None):
        """Cancel the ride"""
        try:
            booking = self.get_object()
            if booking.status in ['COMPLETED', 'CANCELLED']:
                return Response(
                    {'error': 'Cannot cancel completed or already cancelled ride'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            booking.status = 'CANCELLED'
            booking.save()

            # Send notifications
            message = "Your ride has been cancelled"
            try:
                 send_notification(
                        content=message,
                        chat_id=self.booking_service.default_chat_id,
                        email=self.booking_service.default_email
                    )
            except Exception as e:
                logger.error(f"Failed to send notifications: {str(e)}")

            return Response(self.get_serializer(booking).data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )