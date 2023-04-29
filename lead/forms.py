from django import forms

from lead.models import Lead
from user.models import User, District


class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'middle_name', 'region', 'district', 'address', 'birthday', 'phone']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()

        if 'region' in self.data:

            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(region_id=region_id).order_by('title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.country.city_set.order_by('title')


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'middle_name', 'region', 'district', 'address', 'birthday',
                  'phone', 'passport_seria', 'passport_number', 'person_id', 'gender']


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['service', 'payment_method']
