from rest_framework import serializers
from courses.models import Course, CourseChapter, Lesson, Homework, HomeWorkRespond
from users.serializers import CoursesUserSerializer

class HomeWorkRespondSerializer(serializers.HyperlinkedModelSerializer):
    student = CoursesUserSerializer(read_only=True)
    class Meta:
        model = HomeWorkRespond
        fields = '__all__'

class HomeworkSerializer(serializers.HyperlinkedModelSerializer):
    homework_responds = HomeWorkRespondSerializer(read_only=True, many=True)
    class Meta:
        model = Homework
        fields = '__all__'

class LessonSerializer(serializers.HyperlinkedModelSerializer):
    lesson_homeworks = HomeworkSerializer(read_only=True, many=True)
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseChapterSerializer(serializers.HyperlinkedModelSerializer):
    chapter_lessons = LessonSerializer(read_only=True, many=True)
    class Meta:
        model = CourseChapter
        fields = '__all__'

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    course_chapters = CourseChapterSerializer(read_only=True, many=True)
    teachers = CoursesUserSerializer(read_only=True, many=True)
    students = CoursesUserSerializer(read_only=True, many=True)
    class Meta:
        model = Course
        fields = '__all__'
