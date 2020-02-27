from django.urls import path
from blog import views

urlpatterns = [
    path('', views.blog_home, name='home'),
    path('create/', views.create_blog_post, name='create'),
    path('detail/<int:id>/', views.blog_detail, name='detail'),
]
