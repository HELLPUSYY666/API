from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Category, Post
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

