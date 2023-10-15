from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name',
                  'email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)