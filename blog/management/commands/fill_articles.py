from django.core.management.base import BaseCommand, CommandError
from mixer.backend.django import mixer
from faker import Faker
from blog.models import Category, Article, Commentary
from users.models import CoursesUser
import random

class Command(BaseCommand):
    help = 'Adds random filler articles'

    def add_arguments(self, parser):
        parser.add_argument('num_articles', nargs='+', type=int)

    def handle(self, *args, **options):
        fake = Faker()
        num_articles = options['num_articles'][0]
        for _ in range(num_articles):
            thumbnail_url = f'https://picsum.photos/seed/{"".join([random.choice("abcdefgpicsum") for i in range(6)])}/{random.randrange(4, 8)}00/{random.randrange(3, 7)}00'

            users = CoursesUser.objects.all()
            if len(users)<10:
                for _ in range(10):
                    mixer.blend(CoursesUser, password='qwerty')
                users = CoursesUser.objects.all()

            article = mixer.blend(Article, thumbnail=thumbnail_url, author=random.choice(users))

            categories = Category.objects.all()
            if len(categories)<10:
                for _ in range(10):
                    mixer.blend(Category, name=fake.color_name())
                    categories = Category.objects.all()
            categories = random.choices(categories, k=random.randrange(1, 4))
            article.categories.add(*categories)
            article.save()

            for _ in range(random.randrange(1, 14)):
                author = random.choice(users)
                mixer.blend(Commentary, article=article, author=author, text=fake.text())

        self.stdout.write(f'Successfully added {num_articles} articles')
