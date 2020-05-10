from rest_framework import serializers
from courses.models import Course, CourseChapter, Lesson, Homework, HomeWorkRespond, QuizQuestion, QuizOption
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

class QuizOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuizOption
        fields = '__all__'

class QuizQuestionSerializer(serializers.HyperlinkedModelSerializer):
    question_options = QuizOptionSerializer(read_only=True, many=True)
    class Meta:
        model = QuizQuestion
        fields = '__all__'

class LessonSerializer(serializers.HyperlinkedModelSerializer):
    lesson_quiz_questions = QuizQuestionSerializer(read_only=True, many=True)
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
