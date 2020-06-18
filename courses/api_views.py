from rest_framework import viewsets
from courses.models import Course, CourseChapter, Lesson, Homework, HomeWorkRespond
from courses.serializers import CourseSerializer, CourseChapterSerializer, LessonSerializer, HomeworkSerializer, HomeWorkRespondSerializer
from courses.permissions import IsTeacherOrStudentReadOnly, IsStudentOrTeacherReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.db.models import Q

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrStudentReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Course.shown_objects.prefetch_related('course_chapters')
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        elif self.request.user.is_authenticated:
            return self.queryset.filter(Q(teachers__pk=self.request.user.pk) | Q(students__pk=self.request.user.pk)).distinct()
        else:
            return []

class CourseChapterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrStudentReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = CourseChapter.objects.prefetch_related('chapter_lessons')
    serializer_class = CourseChapterSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        elif self.request.user.is_authenticated:
            return self.queryset.filter(Q(course__teachers__pk=self.request.user.pk) | Q(course__students__pk=self.request.user.pk)).distinct()
        else:
            return []

class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrStudentReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Lesson.objects.prefetch_related('lesson_homeworks')
    serializer_class = LessonSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        elif self.request.user.is_authenticated:
            return self.queryset.filter(Q(chapter__course__teachers__pk=self.request.user.pk) | Q(chapter__course__students__pk=self.request.user.pk)).distinct()
        else:
            return []

class HomeworkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStudentOrTeacherReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Homework.objects.prefetch_related('homework_responds')
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        elif self.request.user.is_authenticated:
            return self.queryset.filter(Q(lesson__chapter__course__teachers__pk=self.request.user.pk) | Q(lesson__chapter__course__students__pk=self.request.user.pk)).distinct()
        else:
            return []

class HomeWorkRespondViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrStudentReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = HomeWorkRespond.objects.all()
    serializer_class = HomeWorkRespondSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        elif self.request.user.is_authenticated:
            return self.queryset.filter(Q(homework__lesson__chapter__course__teachers__pk=self.request.user.pk) | Q(homework__lesson__chapter__course__students__pk=self.request.user.pk)).distinct()
        else:
            return []
