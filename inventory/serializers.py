from rest_framework import serializers
from .models import Vehicle, Booking
from datetime import date

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['total_amount']

    def validate(self, data):

        vehicle = data['vehicle']
        start_date = data['start_date']
        end_date = data['end_date']
        phone = data['customer_phone']

        # 1️⃣ Start date not in past
        if start_date < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")

        # 2️⃣ End date after start date
        if end_date <= start_date:
            raise serializers.ValidationError("End date must be after start date.")

        # 3️⃣ Phone validation
        if not phone.isdigit() or len(phone) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")

        # 4️⃣ Prevent double booking
        overlapping = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        if overlapping.exists():
            raise serializers.ValidationError("Vehicle already booked for selected dates.")

        return data

    def create(self, validated_data):

        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        vehicle = validated_data['vehicle']

        days = (end_date - start_date).days
        total = days * vehicle.price_per_day

        validated_data['total_amount'] = total

        booking = Booking.objects.create(**validated_data)

        # After booking, make vehicle unavailable
        vehicle.is_available = False
        vehicle.save()

        return booking