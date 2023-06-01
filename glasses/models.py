from django.db import models

from patient.models import PatientComeHistory
from user.models import User


# Create your models here.


class Glass(models.Model):
    patient = models.ForeignKey(PatientComeHistory, on_delete=models.CASCADE)
    sph_od = models.CharField(max_length=20, null=True, blank=True)
    cyl_od = models.CharField(max_length=20, null=True, blank=True)
    ax_od = models.CharField(max_length=20, null=True, blank=True)
    bliz_od = models.CharField(max_length=20, null=True, blank=True)
    sph_os = models.CharField(max_length=20, null=True, blank=True)
    cyl_os = models.CharField(max_length=20, null=True, blank=True)
    ax_os = models.CharField(max_length=20, null=True, blank=True)
    bliz_os = models.CharField(max_length=20, null=True, blank=True)
    dp = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.patient.last_name} {self.patient.patient.phone}"
