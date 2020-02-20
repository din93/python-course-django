from django.core.management.base import BaseCommand, CommandError
from blog.models import Article, Commentary
import requests, random

class Command(BaseCommand):
    help = 'Adds random filler comments to all articles'

    def handle(self, *args, **options):
        articles = Article.objects.all()
        comments_count = 0
        for article in articles:
            for _ in range(random.randrange(1, 4)):
                comment_text = requests.get(f'https://baconipsum.com/api/?type=meat-and-filler&sentences={random.randrange(1, 3)}&format=text').text
                username = requests.get('http://names.drycodes.com/1').json()[0]
                commentary = Commentary(username=username, text=comment_text, article=article)
                commentary.save()
                comments_count+=1

        self.stdout.write(f'Successfully added {comments_count} comments to various articles')
