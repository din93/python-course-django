from rest_framework import viewsets
from users.models import CoursesUser
from users.serializers import CoursesUserSerializer

class CoursesUserViewSet(viewsets.ModelViewSet):
    queryset = CoursesUser.objects.all()
    serializer_class = CoursesUserSerializer