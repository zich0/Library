from django import forms
from .models import Book, Review
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'year_published', 'cover_image']

# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = ['name', 'bio']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'user', 'text', 'rating']


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

        labels = {
            'username': 'Имя пользователя',
        }

        help_texts = {
            'username':''
        }

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class='form-control', ),
            Field('password1', css_class='form-control', rows=3),
            Field('password2', css_class='form-control', rows=3),
            Submit('submit', 'Ввод', css_class='btn btn-primary')
        )


class LoginForm(forms.Form):

    username = forms.CharField(label='Имя пользователя', max_length=20)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class='form-control'),
            Field('password', css_class='form-control', rows=3),
            Submit('submit', 'Ввод', css_class='btn btn-primary')
        )