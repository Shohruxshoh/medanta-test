from django import forms
from .models import User, PATIENT,ADMINISTRATOR
from django.contrib.auth.forms import UserCreationForm


# Sign Up Form
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'role',
            'region',
            'district',
            'address',
            'email',
            'birthday',
            'username',
            'phone',
            'passport_seria',
            'passport_number',
            'person_id',
            'gender',
            'password1',
            'password2',
        ]


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'middle_name', 'region', 'district', 'role', 'address',
                  'birthday',
                  'phone', 'passport_seria', 'passport_number', 'person_id', 'gender']
