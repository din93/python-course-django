from rest_framework import viewsets
from users.models import CoursesUser
from users.serializers import CoursesUserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

class CoursesUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = CoursesUser.objects.all()
    serializer_class = CoursesUserSerializer