from django.db import models
from service.models import Installment
from user.models import User, PARTNER


# Create your models here.

class BHM(models.Model):
    sum = models.IntegerField()
    is_active = models.BooleanField(default=False)
    start_date = models.DateField()
    stop_date = models.DateField()

    def __str__(self):
        return str(self.sum * 0.7)


class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bhm_sum = models.ForeignKey(BHM, on_delete=models.CASCADE)
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} {self.bhm_sum}"


class Partner(models.Model):
    partner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    credit_card = models.CharField(max_length=19, null=True, blank=True)
    expire_date = models.CharField(max_length=5, null=True, blank=True)
    credit_card_month = models.CharField(default=0, max_length=2, null=True, blank=True)
    credit_card_year = models.CharField(default=0, max_length=2, null=True, blank=True)

    def __str__(self):
        return f"Hamkor: {self.partner}"
