from django.db import models
from service.models import Service
from user.models import User

# Create your models here.

Naqd = 0
Plastik = 1
Muddatli = 2
Qarzga = 3

PAY = (
    (Naqd, "Naqd"),
    (Plastik, "Plastik"),
    (Muddatli, "Muddatli"),
    (Qarzga, "Qarzga")
)


class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    percentage = models.IntegerField(default=0)
    lead_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAY, default=Naqd)

    def get_pay_display(self):
        a = int(self.payment_method)
        return PAY[a][1]

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} To'lash turi:{self.payment_method}"


class QrCodeRegister(models.Model):
    qr_phone = models.CharField(max_length=20)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name
