from django.test import TestCase
from mixer.backend.django import mixer
from courses.models import Course, CourseChapter, Lesson, Homework, HomeWorkRespond, QuizQuestion, QuizOption
from users.models import CoursesUser

class CourseTestCase(TestCase):

    def setUp(self):
        self.course = mixer.blend(Course, title='Test Course')

    def test_get_chapters(self):
        self.assertFalse(self.course.get_chapters())
        chapter1 = mixer.blend(CourseChapter, title='Test Chapter 1', course=self.course)
        self.assertListEqual(
            list(self.course.get_chapters()),
            [chapter1]
        )
        chapter2 = mixer.blend(CourseChapter, title='Test Chapter 2', course=self.course)
        self.assertListEqual(
            list(self.course.get_chapters()),
            [chapter1, chapter2]
        )
        self.assertEqual(self.course.get_chapters()[0].title, 'Test Chapter 1')

    def test_fill_initial(self):
        self.assertFalse(self.course.get_chapters())
        self.course.fill_course_initial()
        self.assertTrue(len(self.course.get_chapters())==1)
        
class CourseChapterTestCase(TestCase):

    def test_get_questions(self):
        chapter = mixer.blend(CourseChapter)
        lesson1 = mixer.blend(Lesson, title='Test Lesson 1', chapter=chapter)
        self.assertListEqual(
            list(chapter.get_lessons()),
            [lesson1]
        )
        lesson2 = mixer.blend(Lesson, title='Test Lesson 2', chapter=chapter)
        self.assertListEqual(
            list(chapter.get_lessons()),
            [lesson1, lesson2]
        )
        self.assertEqual(chapter.get_lessons()[1].title, 'Test Lesson 2')

class LessonTestCase(TestCase):

    def setUp(self):
        self.lesson = mixer.blend(Lesson)

    def test_get_questions(self):
        
        quiz_question1 = mixer.blend(QuizQuestion, lesson=self.lesson)
        self.assertListEqual(
            list(self.lesson.get_questions()),
            [quiz_question1]
        )
        quiz_question2 = mixer.blend(QuizQuestion, text='Test Question 2', lesson=self.lesson)
        self.assertListEqual(
            list(self.lesson.get_questions()),
            [quiz_question1, quiz_question2]
        )
        self.assertEqual(self.lesson.get_questions()[1].text, 'Test Question 2')

    def test_get_homework(self):
        homework = mixer.blend(Homework, text='Test Homework', lesson=self.lesson)

        self.assertEqual(self.lesson.get_homework(), homework)
        self.assertEqual(self.lesson.get_homework().text, 'Test Homework')

class QuizQuestionsTestCase(TestCase):

    def test_get_options(self):
        quiz_question = mixer.blend(QuizQuestion)
        quiz_option1 = mixer.blend(QuizOption, text='Test Option 1', question=quiz_question)
        self.assertListEqual(
            list(quiz_question.get_options()),
            [quiz_option1]
        )
        quiz_option2 = mixer.blend(QuizOption, question=quiz_question)
        self.assertListEqual(
            list(quiz_question.get_options()),
            [quiz_option1, quiz_option2]
        )
        self.assertEqual(quiz_question.get_options()[0].text, 'Test Option 1')

class HomeWorkTestCase(TestCase):

    def setUp(self):
        self.homework = mixer.blend(Homework)

    def test_get_responds(self):
        homework_respond1 = mixer.blend(HomeWorkRespond, homework=self.homework)
        self.assertListEqual(
            list(self.homework.get_responds()),
            [homework_respond1]
        )
        homework_respond2 = mixer.blend(HomeWorkRespond, homework=self.homework)
        self.assertListEqual(
            list(self.homework.get_responds()),
            [homework_respond1, homework_respond2]
        )

    def test_get_responded_students(self):
        homework_respond1 = mixer.blend(HomeWorkRespond, homework=self.homework)
        homework_respond2 = mixer.blend(HomeWorkRespond, homework=self.homework)
        self.assertListEqual(
            list(self.homework.get_responded_students()),
            [homework_respond1.student, homework_respond2.student]
        )
