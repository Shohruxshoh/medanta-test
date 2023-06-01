from django.db import models
from service.models import Service
from user.models import User


# Create your models here.


class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    sum_total = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} {self.sum_total}"


class Partner(models.Model):
    partner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    credit_card = models.CharField(max_length=19, null=True, blank=True)
    expire_date = models.CharField(max_length=5, null=True, blank=True)
    credit_card_month = models.CharField(default=0, max_length=2, null=True, blank=True)
    credit_card_year = models.CharField(default=0, max_length=2, null=True, blank=True)

    def __str__(self):
        return f"Hamkor: {self.partner}"


class PartnerAndPatient(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
