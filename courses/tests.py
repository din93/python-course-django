from django.test import TestCase, Client
from mixer.backend.django import mixer
from courses.models import Course, CourseChapter, Lesson, Homework, HomeWorkRespond
from users.models import CoursesUser

class CourseTestCase(TestCase):

    def setUp(self):
        self.course = mixer.blend(Course, title='Test Course')
        self.client = Client()

    def test_get_chapters(self):
        self.assertTrue(len(self.course.course_chapters.all())==1)
        chapter2 = mixer.blend(CourseChapter, title='Test Chapter 2', course=self.course)
        self.assertListEqual(
            list(self.course.course_chapters.all()),
            [self.course.course_chapters.first(), chapter2]
        )
        self.assertEqual(self.course.course_chapters.all()[1].title, 'Test Chapter 2')

    def test_fill_initial(self):
        course = mixer.blend(Course, title='Test Course')
        self.assertTrue(len(course.course_chapters.all())==1)
        self.assertTrue(len(course.course_chapters.first().chapter_lessons.all())==1)

    def test_api_student_access(self):
        user = CoursesUser.objects.create_user(username='test_user', email='tester@testmail.com', password='qwerty')
        response = self.client.get(f'/api/v0/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 404)

        self.client.login(username='test_user', password='qwerty')
        response = self.client.get(f'/api/v0/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 404)
        
        self.course.students.add(user)
        response = self.client.get(f'/api/v0/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_teacher_access(self):
        user = CoursesUser.objects.create_user(username='test_user', email='tester@testmail.com', password='qwerty')
        response = self.client.get(f'/api/v0/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 404)

        self.client.login(username='test_user', password='qwerty')
        response = self.client.get(f'/api/v0/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 404)
        
        self.course.teachers.add(user)
        response = self.client.get(f'/api/v0/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 200)

class CourseChapterTestCase(TestCase):

    def test_get_lessons(self):
        chapter = mixer.blend(CourseChapter)
        lesson1 = mixer.blend(Lesson, title='Test Lesson 1', chapter=chapter)
        self.assertListEqual(
            list(chapter.chapter_lessons.all()),
            [lesson1]
        )
        lesson2 = mixer.blend(Lesson, title='Test Lesson 2', chapter=chapter)
        self.assertListEqual(
            list(chapter.chapter_lessons.all()),
            [lesson1, lesson2]
        )
        self.assertEqual(chapter.chapter_lessons.all()[1].title, 'Test Lesson 2')

class LessonTestCase(TestCase):

    def setUp(self):
        self.lesson = mixer.blend(Lesson)

    def test_get_homework(self):
        homework = mixer.blend(Homework, text='Test Homework', lesson=self.lesson)

        self.assertEqual(self.lesson.get_homework, homework)
        self.assertEqual(self.lesson.get_homework.text, 'Test Homework')

class HomeWorkTestCase(TestCase):

    def setUp(self):
        self.homework = mixer.blend(Homework)

    def test_get_responds(self):
        homework_respond1 = mixer.blend(HomeWorkRespond, homework=self.homework)
        self.assertListEqual(
            list(self.homework.homework_responds.all()),
            [homework_respond1]
        )
        homework_respond2 = mixer.blend(HomeWorkRespond, homework=self.homework)
        self.assertListEqual(
            list(self.homework.homework_responds.all()),
            [homework_respond1, homework_respond2]
        )

    def test_get_responded_students(self):
        homework_respond1 = mixer.blend(HomeWorkRespond, homework=self.homework)
        homework_respond2 = mixer.blend(HomeWorkRespond, homework=self.homework)
        self.assertListEqual(
            list(self.homework.get_responded_students()),
            [homework_respond1.student, homework_respond2.student]
        )
