from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_service_provider = models.BooleanField(default=False)  # Identify if the user is a service provider

class ServiceProvider(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='service_provider')
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client')

    def __str__(self):
        return self.user.username

class Service(models.Model):
    SERVICE_CATEGORIES = [
        ('Dance', 'Dance'),
        ('Music', 'Music'),
        ('MC', 'Master of Ceremonies'),
        # Add more categories as needed
    ]
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=SERVICE_CATEGORIES)

    def __str__(self):
        return f"{self.name} by {self.provider.user.username}"

class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS)

    def __str__(self):
        return f"Booking on {self.booking_date} for {self.client.user.username}"

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.booking.client.user.username} for Booking ID {self.booking.id}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        # Add more methods as needed
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    method = models.CharField(max_length=50, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"Payment of {self.amount} on {self.payment_date} for Booking ID {self.booking.id}"

class EventDetails(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='event_details')
    event_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    event_date = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"Event on {self.event_date} at {self.location}"
