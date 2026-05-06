from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": True}))


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]
