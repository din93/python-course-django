from django.db import models
from users.models import CoursesUser
from django.utils.functional import cached_property

class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class ShownObjectsManager(models.Manager):
    def get_queryset(self):
        all_objects = super().get_queryset()
        return all_objects.filter(is_shown=True)

class HideableMixin(models.Model):
    objects = models.Manager()
    shown_objects = ShownObjectsManager()
    is_shown = models.BooleanField(default=True)
    class Meta:
        abstract = True

class Course(TimeStamp, HideableMixin):
    title = models.CharField(max_length=50, unique=False)
    thumbnail = models.ImageField(upload_to='thumbnails/courses/', blank=True, null=True)
    overview = models.TextField(blank=True)
    prereqs = models.TextField(blank=True)
    teachers = models.ManyToManyField(CoursesUser, related_name='teacher_courses', blank=True)
    students = models.ManyToManyField(CoursesUser, related_name='student_courses', blank=True)
    participation_requests = models.ManyToManyField(CoursesUser, related_name='participation_requests_courses', blank=True)

    def __str__(self):
        return self.title

    @cached_property
    def display_teachers(self):
        teachers = self.teachers.all()
        return ', '.join([teacher.username for teacher in teachers])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not len(self.course_chapters.all()):
            new_chapter = CourseChapter.objects.create(
                title = 'Название блока',
                number = 1,
                course = self
            )
            new_lesson = Lesson.objects.create(
                title = 'Название урока',
                chapter = new_chapter,
                number = 1,
                estimated_time_min = 10,
                description = 'Текст урока'
            )
            new_homework = Homework.objects.create(
                lesson = new_lesson,
                text = 'Текст домашнего задания',
                points = 10
            )

    @cached_property
    def get_thumbnail_url(self):
        return self.thumbnail if 'http' in self.thumbnail.url else self.thumbnail.url

    @cached_property
    def has_thumbnail(self):
        return bool(self.thumbnail)

    def is_user_teacher(self, user):
        return self.teachers.filter(id=user.id).exists()

    def is_user_student(self, user):
        return self.students.filter(id=user.id).exists()

class CourseChapter(models.Model):
    title = models.CharField(max_length=50, unique=False)
    number = models.PositiveSmallIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_chapters')
    finishers = models.ManyToManyField(CoursesUser, related_name='finished_course_chapters')

    def __str__(self):
        return self.title

    def is_user_teacher(self, user):
        return self.course.is_user_teacher(user)

    def is_user_student(self, user):
        return self.course.is_user_student(user)

class Lesson(TimeStamp, HideableMixin):
    title = models.CharField(max_length=50, unique=False)
    thumbnail = models.ImageField(upload_to='thumbnails/courses/lessons/', blank=True, null=True)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, related_name='chapter_lessons')
    number = models.PositiveSmallIntegerField()
    estimated_time_min = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    @cached_property
    def get_homework(self):
        return Homework.objects.filter(lesson=self).first()

    def is_user_teacher(self, user):
        return self.chapter.course.is_user_teacher(user)

    def is_user_student(self, user):
        return self.chapter.course.is_user_student(user)

class Homework(TimeStamp):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_homeworks')
    text = models.TextField()
    points = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.text} from lesson: {self.lesson}'

    def get_responded_students(self):
        hw_responds = self.homework_responds.all()
        return [hw_respond.student for hw_respond in hw_responds]
    
    def is_user_teacher(self, user):
        return self.lesson.chapter.course.is_user_teacher(user)

    def is_user_student(self, user):
        return self.lesson.chapter.course.is_user_student(user)

class HomeWorkRespond(TimeStamp):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='homework_responds')
    student = models.ForeignKey(CoursesUser, on_delete=models.CASCADE, related_name='homework_responds')
    text = models.TextField()
    file_attachment = models.FileField(blank=True, upload_to='files/courses/homeworks/')
    is_public = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text} to homework: {self.homework}'
    
    def is_user_teacher(self, user):
        return self.homework.lesson.chapter.course.is_user_teacher(user)

    def is_user_student(self, user):
        return self.homework.lesson.chapter.course.is_user_student(user)

class HWRespondCommentary(TimeStamp, HideableMixin):
    author = models.ForeignKey(CoursesUser, on_delete=models.CASCADE, related_name='user_commentaries_to_homework_respond')
    text = models.CharField('Текст комментария', max_length=200)
    homework_respond = models.ForeignKey(HomeWorkRespond, on_delete=models.CASCADE, related_name='homework_respond_commentaries')

    def __str__(self):
        return f'From "{self.author.username}": {self.text}'

    class Meta:
        verbose_name_plural = 'HWRespondCommentaries'