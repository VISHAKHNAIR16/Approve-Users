from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('vehicle_name', 'pickup_location', 'dropoff_location', 'date', 'price')
    search_fields = ('vehicle_name', 'pickup_location', 'dropoff_location')
    list_filter = ('date', 'pickup_location', 'dropoff_location')
    ordering = ('date',)