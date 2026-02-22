from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Vehicle, Booking
from .serializers import VehicleSerializer, BookingSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        brand = self.request.query_params.get('brand')
        fuel_type = self.request.query_params.get('fuel_type')
        is_available = self.request.query_params.get('is_available')

        if brand:
            queryset = queryset.filter(brand__iexact=brand)

        if fuel_type:
            queryset = queryset.filter(fuel_type__iexact=fuel_type)

        if is_available:
            queryset = queryset.filter(is_available=is_available.lower() == 'true')

        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
