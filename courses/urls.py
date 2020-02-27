from django.urls import path
from courses import views

urlpatterns = [
    path('list/', views.courses_list, name='list'),
    path('lessons/<int:course_id>/', views.course_lessons, name='lessons'),
    path('detail/<int:course_id>/', views.course_detail, name='detail'),
]
