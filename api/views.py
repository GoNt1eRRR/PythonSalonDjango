# views.py
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from beauty_salon.models import (
    CustomUser, Salon, Procedure,
    Specialist, Availability, Booking
)
from .serializers import (
    CustomUserSerializer, SalonSerializer, ProcedureSerializer,
    SpecialistSerializer, AvailabilitySerializer,
    BookingSerializer
)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class SalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer


class ProcedureViewSet(viewsets.ModelViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer


class SpecialistViewSet(viewsets.ModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['salons', 'procedures']


class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['specialist', 'salon', 'is_booked']


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['salon', 'procedure', 'client', 'confirmed']

