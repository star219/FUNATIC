from django import forms 
from django.contrib.auth.forms import UserCreationForm

from .models import UserAccount


class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ["username", "email", "password1", "password2"]