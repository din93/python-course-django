from django.core.management.base import BaseCommand, CommandError
from blog.models import Article

class Command(BaseCommand):
    help = 'Delete all articles'

    def handle(self, *args, **options):
        articles = Article.objects.all()
        articles.delete()

        self.stdout.write(f'Successfully deleted all articles')
