from django.core.management.base import BaseCommand, CommandError
from blog.models import Article, Commentary
from users.models import CoursesUser
import requests, random

class Command(BaseCommand):
    help = 'Adds random filler comments to all articles'

    def handle(self, *args, **options):
        articles = Article.objects.all()
        comments_count = 0
        users = CoursesUser.objects.all()
        for article in articles:
            for _ in range(random.randrange(1, 4)):
                comment_text = requests.get(f'https://baconipsum.com/api/?type=meat-and-filler&sentences={random.randrange(1, 3)}&format=text').text
                author = random.choice(users)
                commentary = Commentary(author=author, text=comment_text, article=article)
                commentary.save()
                comments_count+=1

        self.stdout.write(f'Successfully added {comments_count} comments to various articles')
