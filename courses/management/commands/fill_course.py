from django.core.management.base import BaseCommand, CommandError
from courses import models
import requests, random

class Command(BaseCommand):
    help = 'Adds a random filler course'

    def handle(self, *args, **options):
        course_title = requests.get('https://baconipsum.com/api/?type=meat-and-filler&sentences=1&format=text').text

        new_course = models.Course(
            title = course_title,
            overview = requests.get('https://fish-text.ru/get?type=sentence&number=6').json()['text'],
            prereqs = requests.get('https://fish-text.ru/get?type=sentence&number=3').json()['text']
        )
        new_course.save()

        for chapter_number in range(random.randrange(3, 6)):
            new_chapter = models.CourseChapter(
                title = requests.get('https://baconipsum.com/api/?type=meat-and-filler&sentences=1&format=text').text,
                number = chapter_number+1,
                course = new_course
            )
            new_chapter.save()
            for lesson_number in range(random.randrange(2, 5)):
                new_lesson = models.Lesson(
                    title = requests.get('https://baconipsum.com/api/?type=meat-and-filler&sentences=1&format=text').text,
                    chapter = new_chapter,
                    number = lesson_number+1,
                    estimated_time_min = (lesson_number+1)*10,
                    description = requests.get('https://fish-text.ru/get?type=sentence&number=6').json()['text']
                )
                new_lesson.save()
                new_homework = models.Homework(
                    lesson = new_lesson,
                    text = requests.get('https://fish-text.ru/get?type=sentence&number=6').json()['text'],
                    points = (lesson_number+1)*(chapter_number+1)*10
                )
                new_homework.save()
                for _ in range(random.randrange(1, 4)):
                    new_quiz_question = models.QuizQuestion(
                        lesson = new_lesson,
                        text = requests.get('https://fish-text.ru/get?type=sentence&number=1').json()['text'][:-1]+'?',
                        points = (lesson_number+1)*4+(chapter_number+1)
                    )
                    new_quiz_question.save()
                    for answer_index in range(5):
                        new_quiz_option = models.QuizOption(
                            question = new_quiz_question,
                            text = requests.get('https://fish-text.ru/get?type=sentence&number=1').json()['text'],
                            is_right = answer_index==3
                        )
                        new_quiz_option.save()

        self.stdout.write(f'Successfully added a course named "{course_title}"')
