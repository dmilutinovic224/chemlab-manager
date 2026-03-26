from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from Projekat.accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20,  required=False, label='Telefon')
    institution = forms.CharField(max_length=200,  required=False, label='Institucija')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'institution', 'password1', 'password2']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError('email postoji')
            return email

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'institution', 'bio']

