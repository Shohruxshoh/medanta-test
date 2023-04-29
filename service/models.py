from django.db import models
from user.models import User, Clinic


# Create your models here.

class ServicePrice(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    price = models.IntegerField(default=1)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.price)


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_user')
    service_price = models.ForeignKey(ServicePrice, on_delete=models.CASCADE, related_name='service_service_price')
    title = models.CharField(max_length=250)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Installment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    month = models.IntegerField(default=0)
    percent = models.IntegerField(default=10)
    month_pay = models.IntegerField(default=0)
    total_pay = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_archive = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service.title}  oy: {self.month} foiz: {self.percent}"


class PayInstalmentCombine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)


class PayInstallmentPeriod(models.Model):
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='pay_installment_period_to_service')
    start_date = models.DateField()
    pay_date = models.DateField(default='1900-01-01')
    sum = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} summa: {self.sum}"


class Debts(models.Model):
    pay_installment_period = models.ForeignKey(PayInstallmentPeriod, on_delete=models.CASCADE)
    amount_received = models.IntegerField(default=0)  # olingan summa
