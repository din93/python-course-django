from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CoursesUser

class LoginUserForm(forms.ModelForm):
    class Meta:
        model = CoursesUser
        fields = [
            'username',
            'email',
            'avatar',
            'password'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CoursesUser
        fields = ['email', 'username', 'avatar', 'password1', 'password2']
