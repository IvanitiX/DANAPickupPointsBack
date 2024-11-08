from django.db import models

from pickup_point.models import PickupPoint

class Report(models.Model):
    related_pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name='reports', null=True)
    description = models.TextField(null=False)