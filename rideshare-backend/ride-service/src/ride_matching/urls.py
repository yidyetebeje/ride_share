from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'ride-requests', views.RideRequestViewSet)
router.register(r'drivers', views.DriverViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

