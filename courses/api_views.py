from rest_framework import viewsets
from courses.models import Course, CourseChapter, Lesson, Homework, HomeWorkRespond, QuizQuestion, QuizOption
from courses.serializers import CourseSerializer, CourseChapterSerializer, LessonSerializer, HomeworkSerializer, HomeWorkRespondSerializer, QuizQuestionSerializer, QuizOptionSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.shown_objects.all()
    serializer_class = CourseSerializer

class CourseChapterViewSet(viewsets.ModelViewSet):
    queryset = CourseChapter.objects.all()
    serializer_class = CourseChapterSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class HomeWorkRespondViewSet(viewsets.ModelViewSet):
    queryset = HomeWorkRespond.objects.all()
    serializer_class = HomeWorkRespondSerializer

class QuizQuestionViewSet(viewsets.ModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer

class QuizOptionViewSet(viewsets.ModelViewSet):
    queryset = QuizOption.objects.all()
    serializer_class = QuizOptionSerializer