from django.test import Client, TestCase
from users.models import CoursesUser
from mixer.backend.django import mixer
from blog.models import Article

class BlogViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()        

    def test_login(self):
        self.user = CoursesUser.objects.create_user(username='test_user', email='tester@testmail.com', password='qwerty')
        response = self.client.post('/users/login/', {'username': 'test_user', 'password': '123456'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/users/login/', {'username': 'test_User', 'password': 'qwerty'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/users/login/', {'username': 'test_user', 'password': 'qwerty'})
        self.assertEqual(response.status_code, 302)
    
    def test_get_context(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('categories' in response.context)

    def test_blogger_access(self):
        user = CoursesUser.objects.create_user(username='test_user', email='tester@testmail.com', password='qwerty')
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test_user', password='qwerty')
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)

    def test_commentator_access(self):
        user = CoursesUser.objects.create_user(username='test_user', email='tester@testmail.com', password='qwerty')
        self.article = mixer.blend(Article)

        response = self.client.post(f'/blog/create_comment/{self.article.id}/', {'text': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/create_comment/{self.article.id}/')

        self.client.login(username='test_user', password='qwerty')
        response = self.client.post(f'/blog/create_comment/{self.article.id}/', {'text': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/blog/detail/{self.article.id}/')
