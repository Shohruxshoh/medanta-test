from django.forms import ModelForm

from service.models import Service, Installment, PayInstallmentPeriod, PayInstalmentCombine
from user.models import User


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'service_price']


class InstallmentForm(ModelForm):
    class Meta:
        model = Installment
        fields = ['service', 'month', 'percent', 'is_active', 'is_archive']


class PayInstalmentCombineForm(ModelForm):
    class Meta:
        model = PayInstalmentCombine
        fields = ['user', 'installment', "service"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['user'].queryset = User.objects.none()
    #
    #     if 'user' in self.data:
    #         self.fields['user'].queryset = User.objects.all()
    #
    #     elif self.instance.pk:
    #         self.fields['user'].queryset = User.objects.all().filter(pk=self.instance.language.pk)
