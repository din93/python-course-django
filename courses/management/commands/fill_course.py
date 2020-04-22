from django.core.management.base import BaseCommand, CommandError
from courses import models
import requests, random

class Command(BaseCommand):
    help = 'Adds a random filler course'

    def handle(self, *args, **options):
        course_title = requests.get('http://asdfast.beobit.net/api/?type=word').json()['text'].replace('.', '')
        thumbnail_url = f'https://picsum.photos/seed/{"".join([random.choice("abcdefgpicsum") for i in range(6)])}/750/500'
        text_url = random.choice([
            f'https://baconipsum.com/api/?type=meat-and-filler&paras={random.randrange(3, 6)}&format=text',
            f'https://loripsum.net/api/{random.randrange(3, 6)}/short/plaintext/'
        ])

        new_course = models.Course(
            title = course_title,
            overview = requests.get(text_url).text,
            prereqs = requests.get('http://asdfast.beobit.net/api/?type=word&length=30').json()['text'].replace('. ', '\n'),
            thumbnail = thumbnail_url
        )
        new_course.save()

        for chapter_number in range(random.randrange(3, 6)):
            new_chapter = models.CourseChapter(
                title = requests.get('http://asdfast.beobit.net/api/?type=word').json()['text'].replace('.', ''),
                number = chapter_number+2,
                course = new_course
            )
            new_chapter.save()
            for lesson_number in range(random.randrange(2, 5)):
                new_lesson = models.Lesson(
                    title = requests.get('http://asdfast.beobit.net/api/?type=word').json()['text'].replace('.', ''),
                    chapter = new_chapter,
                    number = lesson_number+1,
                    estimated_time_min = (lesson_number+1)*10,
                    description = requests.get(f'https://loripsum.net/api/{random.randrange(3, 6)}/short/plaintext/').text
                )
                new_lesson.save()
                new_homework = models.Homework(
                    lesson = new_lesson,
                    text = requests.get(f'https://loripsum.net/api/{random.randrange(3, 6)}/short/plaintext/').text,
                    points = (lesson_number+1)*(chapter_number+1)*10
                )
                new_homework.save()
                for _ in range(random.randrange(1, 4)):
                    new_quiz_question = models.QuizQuestion(
                        lesson = new_lesson,
                        text = requests.get('http://asdfast.beobit.net/api/?type=word').json()['text'].replace('.', '')+'?',
                        points = (lesson_number+1)*4+(chapter_number+1)
                    )
                    new_quiz_question.save()
                    for answer_index in range(5):
                        new_quiz_option = models.QuizOption(
                            question = new_quiz_question,
                            text = requests.get('http://asdfast.beobit.net/api/?type=word').json()['text'],
                            is_right = answer_index==3
                        )
                        new_quiz_option.save()

        self.stdout.write(f'Successfully added a course named "{course_title}"')
