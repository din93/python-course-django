from django.core.management.base import BaseCommand, CommandError
from mixer.backend.django import mixer
from faker import Faker
from blog.models import Article, Commentary
from users.models import CoursesUser
import random

class Command(BaseCommand):
    help = 'Adds random filler comments to all articles'

    def handle(self, *args, **options):
        fake = Faker()
        articles = Article.objects.all()
        comments_count = 0
        users = CoursesUser.objects.all()
        for article in articles:
            for _ in range(random.randrange(1, 4)):
                author = random.choice(users)
                mixer.blend(Commentary, article=article, author=author, text=fake.text())
                comments_count+=1

        self.stdout.write(f'Successfully added {comments_count} comments to various articles')
