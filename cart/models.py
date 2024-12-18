# models.py
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Listing(models.Model):  # This is your cart_listing table.
    # Fields of the cart_listing table
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    date = models.DateField()
    vehicle_name = models.CharField(max_length=100)
    model_no = models.CharField(max_length=50)
    pax = models.IntegerField()
    capacity = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'cart_listing'  # Ensure the db_table name is correctly matched

    def _str_(self):
        return f"{self.vehicle_name} ({self.model_no}) - {self.pickup_location} to {self.dropoff_location}"

class CartShip(models.Model):
    listing_option = models.ForeignKey(Listing, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_ship'

    def _str_(self):
        return f"CartShip item: {self.listing_option.vehicle_name} ({self.quantity})"