from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserViewSet, SalonViewSet, ProcedureViewSet,
    SalonProcedureViewSet, SpecialistViewSet,
    AvailabilityViewSet, BookingViewSet
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'salons', SalonViewSet, basename='salons')
router.register(r'procedures', ProcedureViewSet, basename='procedures')
router.register(r'salon-procedures', SalonProcedureViewSet, basename='salon-procedures')
router.register(r'specialists', SpecialistViewSet, basename='specialists')
router.register(r'availabilities', AvailabilityViewSet, basename='availabilities')
router.register(r'bookings', BookingViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
]
