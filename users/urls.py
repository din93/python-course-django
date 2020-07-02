from django.urls import path
from django.contrib.auth.views import LogoutView
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('profile/<int:pk>', views.UserDetailView.as_view(), name='profile'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),
    path('update_token/', views.update_token, name='update_token')
]
