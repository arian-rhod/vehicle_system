

# Register your models here.
from django.contrib import admin
from .models import Vehicle, Booking

admin.site.register(Vehicle)
admin.site.register(Booking)