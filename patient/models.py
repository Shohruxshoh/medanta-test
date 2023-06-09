import qrcode
from django.core.files import File
from django.db import models
from deposit.models import Partner
from user.models import User, Clinic
from io import BytesIO


# Create your models here.
class CardToUser(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="card_to_user_patient")
    card_id = models.CharField(max_length=20)

    class Meta:
        unique_together = [['clinic', 'card_id']]

    def __str__(self):
        return f"{self.card_id} | {self.clinic}"


class PatientComeHistory(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    come_date = models.DateTimeField(auto_now_add=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.patient.phone


# class PatientImage(models.Model):
#     patient = models.ForeignKey(PatientComeHistory, on_delete=models.CASCADE)
#     image = models.FileField(upload_to='media/', null=True, blank=True)


class NextCome(models.Model):
    patient_come_history = models.ForeignKey(PatientComeHistory, on_delete=models.CASCADE)
    next_come = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bemor: {self.patient_come_history.patient.phone} qachon kelgani: {self.patient_come_history.come_date}'


class QRCodeRegister(models.Model):
    card_id_qr = models.CharField(max_length=10, null=True, blank=True)
    fio = models.CharField(max_length=200, null=True, blank=True)
    qr_phone = models.CharField(max_length=15)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'Card: {self.card_id_qr} FIO: {self.fio} Telefon: {self.qr_phone}'


class QRCodePartner(models.Model):  # PartnerQRCode
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True)
    fio = models.CharField(max_length=200, null=True, blank=True)
    qr_phone = models.CharField(max_length=15, unique=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.partner} Bemor:{self.fio}|{self.qr_phone}"


class PhoneCode(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=6)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class QrCodeGenerator1(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True)
    qr_code = models.IntegerField(default=0)
    qr_code_url = models.CharField(max_length=300)
    qr_code_img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.qr_code_url
