from django.contrib import admin
from .models import PaymentMethod, PaymentRecord

admin.site.register(PaymentMethod)
admin.site.register(PaymentRecord)