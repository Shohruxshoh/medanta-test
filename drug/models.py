from django.db import models

from service.models import Service
from user.models import Clinic, User
from patient.models import PatientComeHistory

# Create your models here.
BIR = 1
IKKI = 2
UCH = 3
TURT = 4
BESH = 5
OLTI = 6
YETTI = 7
SAKKIZ = 8
DATE = {
    (BIR, '1'),
    (IKKI, '2'),
    (UCH, '3'),
    (TURT, '4'),
    (BESH, '5'),
    (OLTI, '6'),
    (YETTI, '7'),
    (SAKKIZ, '8')
}


class Drugs(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Pharmacy(models.Model):
    patient = models.ForeignKey(PatientComeHistory, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drugs, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=6, null=True, blank=True)
    between_time = models.CharField(max_length=6, null=True, blank=True)
    lifetime = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    expensive_time = models.CharField(max_length=3, default=BIR, choices=DATE)

    def __str__(self):
        return self.expensive_time


class Operations(models.Model):
    patient = models.ForeignKey(PatientComeHistory, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_active_operations = models.BooleanField(default=True)

    def __str__(self):
        return self.patient.patient.phone
