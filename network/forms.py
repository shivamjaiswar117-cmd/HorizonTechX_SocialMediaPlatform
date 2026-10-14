from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)


class PostForm(forms.Form):
    content = forms.CharField(max_length=280)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar_url")
