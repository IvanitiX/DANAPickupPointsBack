from django.db import models

class Town(models.Model):
    zip_code = models.CharField(max_length=5)
    name = models.CharField(null=False,max_length=256)