from django.db import models

from service.models import Service
from user.models import User


# Create your models here.


class DayAccountant(models.Model):
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    sum_total = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.patient.last_name
