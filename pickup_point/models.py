from django.db import models

from geopy.geocoders import Nominatim

from town.models import Town

# Create your models here.
class PickupPoint(models.Model):
    name = models.CharField(max_length=256, null=False)
    observations = models.CharField(max_length=2048, null=True)

    street = models.CharField(max_length=512, null=False)
    number = models.CharField(max_length=512, null=False, default='s/n')
    floor = models.CharField(max_length=512, null=True, blank=True)
    latitude = models.FloatField(max_length=32, null=True, blank=True)
    longitude = models.FloatField(max_length=32, null=True, blank=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=False)

    def get_coordinates(self):
        "Using geopy package and  Nominatim geocoder to get coordinates from street, number and town"
        geocoder = Nominatim(user_agent="dana_pickup_points", timeout=10)
        location = geocoder.geocode(f"{self.street} {self.number}, {self.town.name}")

        if location is not None:
            self.latitude = location.latitude
            self.longitude = location.longitude
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.latitude is None or self.longitude is None:
            self.get_coordinates()
