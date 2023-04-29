from django import forms

from patient.models import QRCodeRegister, QRCodePartner


class QRCodeRegisterForm(forms.ModelForm):
    class Meta:
        model = QRCodeRegister
        fields = ['card_id_qr', 'fio', 'qr_phone']


class QRCodePartnerForm(forms.ModelForm):
    class Meta:
        model = QRCodePartner
        fields = ['partner', 'fio', 'qr_phone']
