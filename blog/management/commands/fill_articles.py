from django.core.management.base import BaseCommand, CommandError
from blog.models import Category, Article, Commentary
import requests, random

class Command(BaseCommand):
    help = 'Adds random filler articles'

    def add_arguments(self, parser):
        parser.add_argument('num_articles', nargs='+', type=int)

    def handle(self, *args, **options):
        num_articles = options['num_articles'][0]
        for _ in range(num_articles):
            title = requests.get('http://asdfast.beobit.net/api/?type=word').json()['text'].replace('.', '')
            text_url = random.choice([
                f'https://baconipsum.com/api/?type=meat-and-filler&paras={random.randrange(3, 6)}&format=text',
                f'https://loripsum.net/api/{random.randrange(3, 6)}/short/plaintext/'
            ])
            text = requests.get(text_url).text

            thumbnail_url = f'https://picsum.photos/seed/{"".join([random.choice("abcdefgpicsum") for i in range(6)])}/{random.randrange(4, 8)}00/{random.randrange(3, 7)}00'

            new_article = Article(title=title, text=text, thumbnail=thumbnail_url)
            new_article.save()
            categories = Category.objects.all()
            if categories.exists():
                categories = random.choices(categories, k=random.randrange(1, 4))
                new_article.categories.add(*categories)
                new_article.save()
            for _ in range(random.randrange(1, 4)):
                comment_text = requests.get(f'https://baconipsum.com/api/?type=meat-and-filler&sentences={random.randrange(1, 3)}&format=text').text
                username = requests.get('http://names.drycodes.com/1').json()[0]
                commentary = Commentary(username=username, text=comment_text, article=new_article)
                commentary.save()

        self.stdout.write(f'Successfully added {num_articles} articles')
