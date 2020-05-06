from rest_framework import serializers
from users.models import CoursesUser

class CoursesUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CoursesUser
        fields = ['username', 'avatar']