from django.contrib import admin
from .models import CustomUser, Client, ServiceProvider

admin.site.register(CustomUser)
admin.site.register(Client)
admin.site.register(ServiceProvider)