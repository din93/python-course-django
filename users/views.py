from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, reverse_lazy
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from users.forms import LoginUserForm, RegistrationForm, UpdateAvatarForm
from users.models import CoursesUser
from courses.models import Course
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class CreateUserView(CreateView):
    model = CoursesUser
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    model = CoursesUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['student_courses'] = Course.objects.filter(Q(students__pk=self.request.user.pk))
        context['teacher_courses'] = Course.objects.filter(Q(teachers__pk=self.request.user.pk))
        context['update_avatar_form'] = UpdateAvatarForm
        return context

@api_view(['POST'])
def update_token(request):
    user = request.user
    if hasattr(user, 'auth_token'):
        user.auth_token.delete()
    Token.objects.create(user=user)
    return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': user.pk}))

@api_view(['POST'])
def update_avatar(request):
    form = UpdateAvatarForm(request.POST, request.FILES)
    if form.is_valid():
        request.user.avatar = form.cleaned_data['avatar']
        request.user.save()

    return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': request.user.pk}))
