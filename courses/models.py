from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/avatars/courses/', blank=True)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/avatars/courses/', blank=True)

class Course(models.Model):
    title = models.CharField(max_length=50, unique=False)
    thumbnail = models.ImageField(upload_to='static/thumbnails/courses/', blank=True)
    overview = models.TextField(blank=True)
    prereqs = models.TextField(blank=True)
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(Student)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_shown = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class CourseChapter(models.Model):
    title = models.CharField(max_length=50, unique=False)
    number = models.PositiveSmallIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    finishers = models.ManyToManyField(Student)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=50, unique=False)
    thumbnail = models.ImageField(upload_to='static/thumbnails/courses/lessons/', blank=True)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    estimated_time_min = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_shown = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField()
    points = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.text

class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_right = models.BooleanField()

    def __str__(self):
        return self.text

class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField()
    points = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.text} from lesson: {self.lesson}'

class HomeWorkRespond(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    text = models.TextField()
    file_attachment = models.FileField(blank=True)
    is_public = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text} to homework: {self.homework}'
