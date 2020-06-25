"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import courses
from rest_framework import routers
from blog.api_views import ArticleViewSet, CommentaryViewSet, CategoryViewSet
from courses.api_views import CourseViewSet, CourseChapterViewSet, LessonViewSet, HomeworkViewSet, HomeWorkRespondViewSet
from users.api_views import CoursesUserViewSet

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'commentaries', CommentaryViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'course_chapters', CourseChapterViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'homeworks', HomeworkViewSet)
router.register(r'homework_responds', HomeWorkRespondViewSet)
router.register(r'users', CoursesUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v0/', include(router.urls)),
    path('', courses.views.CoursesMain.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
