from django.test import TestCase
from mixer.backend.django import mixer
from blog.models import Article, Category, Commentary
from users.models import CoursesUser

class ArticleTestCase(TestCase):

    def setUp(self):
        self.user = mixer.blend(CoursesUser, username='Tester')
        self.article = mixer.blend(Article, title='Test Article', author=self.user)

    def test_user_attaching(self):
        self.assertEqual(self.article.author, self.user)
        self.assertEqual(self.article.author.username, 'Tester')

    def test_getting_commentaries(self):
        article_commentaries = [mixer.blend(Commentary, article=self.article) for _ in range(4)]
        self.assertListEqual(
            list(self.article.get_commentaries()),
            list(Commentary.objects.filter(article=self.article).all())
        )
        self.assertTrue(article_commentaries[0] in self.article.get_commentaries())

class CategoryTestCase(TestCase):

    def setUp(self):
        self.category = mixer.blend(Category)
        self.article1 = mixer.blend(Article)
        self.article2 = mixer.blend(Article)

    def test_category_in_articles(self):
        self.assertFalse(self.category in self.article1.categories.all())
        self.article1.categories.add(self.category)
        self.assertTrue(self.category in self.article1.categories.all())

        self.assertFalse(self.category in self.article2.categories.all())
        self.article2.categories.add(self.category)
        self.assertTrue(self.category in self.article2.categories.all())

class CommentaryTestCase(TestCase):

    def setUp(self):
        self.article = mixer.blend(Article)

    def test_commentary_in_article(self):
        commentary = mixer.blend(Commentary, article=self.article)
        self.assertTrue(commentary in self.article.get_commentaries())

    def test_commentary_not_in_article(self):
        commentary = mixer.blend(Commentary)
        self.assertFalse(commentary in self.article.get_commentaries())
