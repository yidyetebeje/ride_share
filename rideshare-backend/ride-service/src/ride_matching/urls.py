
# ride_matching/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'ride-requests', views.RideRequestViewSet)

urlpatterns = [

    # Ride Request Endpoints
    path('ride-requests/', views.RideRequestViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('ride-requests/<int:pk>/', views.RideRequestViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('ride-requests/<int:pk>/request-ride/', 
         views.RideRequestViewSet.as_view({'post': 'request_ride'})),
    path('ride-requests/<int:pk>/estimate-fare/', 
         views.RideRequestViewSet.as_view({'get': 'estimate_fare'})),

]


