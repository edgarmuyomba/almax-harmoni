from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    contact = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"User: {self.username}"
    
class ServiceProvider(CustomUser):
    service = models.CharField(max_length=50)
    amount = models.IntegerField()

class Client(CustomUser):
    payment_method = models.ForeignKey("payments.PaymentMethod", on_delete=models.SET_NULL, null=True, blank=True)