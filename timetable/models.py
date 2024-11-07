from django.db import models

from pickup_point.models import PickupPoint

class Timetable(models.Model):
    related_pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name='timetables', null=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

class Time(models.Model):
    related_timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='times', null=True)
    start_hour = models.TimeField(null=True)
    end_hour = models.TimeField(null=True)
    open_all_day = models.BooleanField(null=False, default=False)

    def save(self, *args, **kwargs):
        if self.start_hour and self.end_hour and self.start_hour > self.end_hour:
            raise ValueError("La hora de inicio debe ser anterior a la de fin.")
        
        return super().save(*args, **kwargs)


