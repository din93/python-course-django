from django.db import models
from users.models import CoursesUser

class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Course(TimeStamp):
    title = models.CharField(max_length=50, unique=False)
    thumbnail = models.ImageField(upload_to='thumbnails/courses/', blank=True, null=True)
    overview = models.TextField(blank=True)
    prereqs = models.TextField(blank=True)
    teachers = models.ManyToManyField(CoursesUser, related_name='teachers', blank=True)
    students = models.ManyToManyField(CoursesUser, related_name='students', blank=True)
    is_shown = models.BooleanField(default=True)

    def get_chapters(self):
        return CourseChapter.objects.filter(course=self)

    def __str__(self):
        return self.title

class CourseChapter(models.Model):
    title = models.CharField(max_length=50, unique=False)
    number = models.PositiveSmallIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    finishers = models.ManyToManyField(CoursesUser)

    def get_lessons(self):
        return Lesson.objects.filter(chapter=self)

    def __str__(self):
        return self.title

class Lesson(TimeStamp):
    title = models.CharField(max_length=50, unique=False)
    thumbnail = models.ImageField(upload_to='thumbnails/courses/lessons/', blank=True, null=True)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    estimated_time_min = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    is_shown = models.BooleanField(default=True)

    def get_questions(self):
        return QuizQuestion.objects.filter(lesson=self)

    def get_homework(self):
        return Homework.objects.filter(lesson=self).first()

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField()
    points = models.PositiveSmallIntegerField()

    def get_options(self):
        return QuizOption.objects.filter(question=self)

    def __str__(self):
        return self.text

class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_right = models.BooleanField()

    def __str__(self):
        return self.text

class Homework(TimeStamp):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField()
    points = models.PositiveSmallIntegerField()

    def get_responds(self):
        return HomeWorkRespond.objects.filter(homework=self).all()

    def get_responded_students(self):
        hw_responds = self.get_responds()
        return [hw_respond.student for hw_respond in hw_responds]
    
    def __str__(self):
        return f'{self.text} from lesson: {self.lesson}'

class HomeWorkRespond(TimeStamp):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(CoursesUser, on_delete=models.CASCADE)
    text = models.TextField()
    file_attachment = models.FileField(blank=True, upload_to='files/courses/homeworks/')
    is_public = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text} to homework: {self.homework}'
