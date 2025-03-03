from django import forms
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=128)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

