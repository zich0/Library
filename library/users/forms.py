from django import forms
from .models import UserImage, Favorite
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]


class UserImageChangeForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['image', ]

