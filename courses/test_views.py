from django.test import Client, TestCase
from users.models import CoursesUser
from mixer.backend.django import mixer
from courses.models import Course, Lesson

class CourseTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.lesson = mixer.blend(Lesson)   
        self.course = self.lesson.chapter.course    

    def test_student_access(self):
        user = CoursesUser.objects.create_user(username='test_user', email='tester@testmail.com', password='qwerty')
        response = self.client.get(f'/courses/lessons/{self.course.pk}/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test_user', password='qwerty')
        response = self.client.get(f'/courses/lessons/{self.course.pk}/')
        self.assertEqual(response.status_code, 403)
        
        self.course.students.add(user)
        response = self.client.get(f'/courses/lessons/{self.course.pk}/')
        self.assertEqual(response.status_code, 200)
    
    def test_teacher_access(self):
        user = CoursesUser.objects.create_user(username='test_user', email='tester@testmail.com', password='qwerty')
        response = self.client.get(f'/courses/lessons/{self.course.pk}/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test_user', password='qwerty')
        response = self.client.get(f'/courses/lessons/{self.course.pk}/')
        self.assertEqual(response.status_code, 403)
        
        self.course.teachers.add(user)
        response = self.client.get(f'/courses/lessons/{self.course.pk}/')
        self.assertEqual(response.status_code, 200)
