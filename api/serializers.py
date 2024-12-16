# serializers.py
from rest_framework import serializers
from beauty_salon.models import (
    CustomUser, Salon, Procedure, SalonProcedure,
    Specialist, Availability, Booking
)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'phone_number', 'telegram_id']


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = ['id', 'name', 'address']


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ['id', 'name', 'description']


class SalonProcedureSerializer(serializers.ModelSerializer):
    salon = SalonSerializer(read_only=True)
    procedure = ProcedureSerializer(read_only=True)
    salon_id = serializers.PrimaryKeyRelatedField(
        source='salon', queryset=Salon.objects.all(), write_only=True)
    procedure_id = serializers.PrimaryKeyRelatedField(
        source='procedure', queryset=Procedure.objects.all(), write_only=True)

    class Meta:
        model = SalonProcedure
        fields = ['id', 'salon', 'procedure', 'price', 'salon_id', 'procedure_id']


class SpecialistSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source='user', queryset=CustomUser.objects.filter(role='specialist'), write_only=True
    )
    salons = SalonSerializer(many=True, read_only=True)
    salons_id = serializers.PrimaryKeyRelatedField(
        source='salons', many=True, queryset=Salon.objects.all(), write_only=True
    )
    procedures = ProcedureSerializer(many=True, read_only=True)
    procedures_id = serializers.PrimaryKeyRelatedField(
        source='procedures', many=True, queryset=Procedure.objects.all(), write_only=True
    )

    class Meta:
        model = Specialist
        fields = ['id', 'user', 'salons', 'procedures', 'user_id', 'salons_id', 'procedures_id']


class AvailabilitySerializer(serializers.ModelSerializer):
    specialist = SpecialistSerializer(read_only=True)
    specialist_id = serializers.PrimaryKeyRelatedField(
        source='specialist', queryset=Specialist.objects.all(), write_only=True
    )
    salon = SalonSerializer(read_only=True)
    salon_id = serializers.PrimaryKeyRelatedField(
        source='salon', queryset=Salon.objects.all(), write_only=True
    )

    class Meta:
        model = Availability
        fields = [
            'id', 'specialist', 'salon', 'start_time', 'end_time', 'is_booked',
            'specialist_id', 'salon_id'
        ]


class BookingSerializer(serializers.ModelSerializer):
    salon = SalonSerializer(read_only=True)
    salon_id = serializers.PrimaryKeyRelatedField(
        source='salon', queryset=Salon.objects.all(), write_only=True
    )
    procedure = ProcedureSerializer(read_only=True)
    procedure_id = serializers.PrimaryKeyRelatedField(
        source='procedure', queryset=Procedure.objects.all(), write_only=True
    )
    availability = AvailabilitySerializer(read_only=True)
    availability_id = serializers.PrimaryKeyRelatedField(
        source='availability', queryset=Availability.objects.filter(is_booked=False), write_only=True
    )

    client = CustomUserSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        source='client', queryset=CustomUser.objects.all(), required=False, allow_null=True, write_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'client', 'client_id', 'salon', 'salon_id', 'procedure', 'procedure_id',
            'availability', 'availability_id', 'price', 'phone_number', 'created_at', 'confirmed'
        ]

    def create(self, validated_data):
        availability = validated_data['availability']
        if availability.is_booked:
            raise serializers.ValidationError("This slot is already booked.")

        instance = super().create(validated_data)

        availability.is_booked = True
        availability.save()

        if not instance.price:
            try:
                salon_proc = SalonProcedure.objects.get(salon=instance.salon, procedure=instance.procedure)
                instance.price = salon_proc.price
            except SalonProcedure.DoesNotExist:
                instance.price = 0
            instance.save()

        return instance
