# booking/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # List and Create
    path('', views.BookingViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='booking-list'),
    
    # Detail view
    path('<int:pk>/', views.BookingViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='booking-detail'),

    # Custom actions
    path('<int:pk>/accept_ride/', 
         views.BookingViewSet.as_view({'post': 'accept_ride'}), 
         name='booking-accept'),
    
    path('<int:pk>/start/', 
         views.BookingViewSet.as_view({'post': 'start_ride'}), 
         name='booking-start'),
         
    path('<int:pk>/complete/', 
         views.BookingViewSet.as_view({'post': 'complete_ride'}), 
         name='booking-complete'),
         
    path('<int:pk>/cancel/', 
         views.BookingViewSet.as_view({'post': 'cancel_ride'}), 
         name='booking-cancel'),
]

