from django.core.management.base import BaseCommand, CommandError
from mixer.backend.django import mixer
from faker import Faker
from courses import models
from users.models import CoursesUser
import random

class Command(BaseCommand):
    help = 'Adds a random filler course'

    def handle(self, *args, **options):
        fake = Faker()
        thumbnail_url = f'https://picsum.photos/seed/{"".join([random.choice("abcdefgpicsum") for i in range(6)])}/750/500'
        course = mixer.blend(models.Course, thumbnail=thumbnail_url)
        course.prereqs = course.prereqs.replace('. ', '.\n')
        course.save()
        models.CourseChapter.objects.filter(course=course).first().delete()
    
        for _ in range(random.randrange(6, 20)):
            student = mixer.blend(CoursesUser, password='qwerty')
            course.students.add(student)
        teacher = mixer.blend(CoursesUser, password='qwerty')
        course.teachers.add(teacher)

        for chapter_number in range(random.randrange(3, 6)):
            chapter = mixer.blend(models.CourseChapter, number=chapter_number+1, course=course)

            for lesson_number in range(random.randrange(2, 5)):
                lesson = mixer.blend(models.Lesson, chapter=chapter, number=lesson_number+1)

                homework = mixer.blend(models.Homework, lesson=lesson)

                for student in course.students.all():
                    if random.randint(0, 1) == 1:
                        mixer.blend(models.HomeWorkRespond, homework=homework, student=student)

                for _ in range(random.randrange(1, 4)):
                    
                    quiz_question = mixer.blend(models.QuizQuestion, lesson=lesson)
                    quiz_question.text = quiz_question.text.replace('.', '').capitalize()+'?'
                    quiz_question.save()

                    for answer_index in range(5):
                        mixer.blend(models.QuizOption, text=fake.color_name(), is_right=answer_index==3, question=quiz_question)

        self.stdout.write(f'Successfully added a course named "{course.title}"')
