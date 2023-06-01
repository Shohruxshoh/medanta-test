from django import forms

from drug.models import Operations


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = ['patient', 'service']
