from django.shortcuts import render
from django.contrib.auth.views import LoginView, reverse_lazy
from django.views.generic import CreateView
from users.forms import LoginUserForm, RegistrationForm
from users.models import CoursesUser

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class CreateUserView(CreateView):
    model = CoursesUser
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
