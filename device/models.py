from django.db import models
from patient.models import PatientComeHistory
from user.models import Clinic


# Create your models here.

class DeviceCategory(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DeviceImage(models.Model):
    device = models.ForeignKey(DeviceCategory, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientComeHistory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
