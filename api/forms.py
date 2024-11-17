from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Category, Post, Group
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
