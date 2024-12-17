from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('specialist', 'Specialist'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Salon(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Procedure(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Specialist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='specialist_profile')
    salons = models.ManyToManyField(Salon, related_name='specialists', blank=True)
    procedures = models.ManyToManyField(Procedure, related_name='specialists', blank=True)

    def __str__(self):
        return f"Specialist {self.user.username}"


class Availability(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='availabilities')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.specialist.user.username} at {self.salon.name} from {self.start_time} to {self.end_time}"


class Booking(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings', blank=True, null=True)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='bookings')
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name='bookings')

    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.procedure.name} at {self.salon.name} on {self.availability.start_time}"


@receiver(post_save, sender=Booking)
def update_availability_and_price(instance, created, **kwargs):
    if created:
        instance.price = instance.procedure.price if instance.procedure.price else 0

        if instance.availability:
            instance.availability.is_booked = True
            instance.availability.save()

        instance.save()