from django.core.management.base import BaseCommand, CommandError
from blog.models import Category, Article
import requests, random

class Command(BaseCommand):
    help = 'Adds random filler articles'

    def add_arguments(self, parser):
        parser.add_argument('num_articles', nargs='+', type=int)

    def handle(self, *args, **options):
        num_articles = options['num_articles'][0]
        for _ in range(num_articles):
            title = requests.get('https://baconipsum.com/api/?type=meat-and-filler&sentences=1&format=text').text
            text = requests.get(f'https://baconipsum.com/api/?type=meat-and-filler&paras={random.randrange(3, 6)}&format=text').text

            new_article = Article(title=title, text=text)
            new_article.save()
            categories = Category.objects.all()
            if categories.exists():
                categories = random.choices(categories, k=random.randrange(1, 4))
                new_article.categories.add(*categories)
                new_article.save()

        self.stdout.write(f'Successfully added {num_articles} articles')
