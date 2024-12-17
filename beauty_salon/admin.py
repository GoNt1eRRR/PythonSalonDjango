from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Salon, Procedure, Specialist, Availability, Booking
)
from django import forms


class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['availability'].queryset = Availability.objects.filter(is_booked=False)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'role', 'phone_number', 'telegram_id', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'telegram_id')
    search_fields = ('username', 'phone_number')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'telegram_id')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'telegram_id')}),
    )


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('user', )
    filter_horizontal = ('salons', 'procedures',)


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('specialist', 'salon', 'start_time', 'end_time', 'is_booked')
    list_filter = ('specialist', 'salon', 'is_booked')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm
    list_display = ('client', 'salon', 'procedure', 'availability', 'price', 'confirmed')
    list_filter = ('salon', 'procedure', 'confirmed')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Salon)
admin.site.register(Procedure)