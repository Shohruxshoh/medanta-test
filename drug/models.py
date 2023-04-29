from django.db import models

from user.models import Clinic


# Create your models here.

class Drugs(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    date = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.name
