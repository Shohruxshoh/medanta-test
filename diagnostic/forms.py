from django import forms
from diagnostic.models import *


class VisusForm(forms.ModelForm):
    class Meta:
        model = Visus
        fields = ['bk', 'cd', 'ck']


class OphthalmologyStatusForm(forms.ModelForm):
    class Meta:
        model = OphthalmologyStatus
        fields = ['complaints', 'anamnesis', 'eyelids', 'eyeball', 'conjunctiva', 'cornea', 'front_camera', 'zrachok',
                  'lens', 'vitreous_body', 'ocular_fundus', 'diagnosis']



