from django.core.management.base import BaseCommand, CommandError
from blog.models import Category
import requests, random

class Command(BaseCommand):
    help = 'Adds random filler for categories'

    def add_arguments(self, parser):
        parser.add_argument('num_categories', nargs='+', type=int)

    def handle(self, *args, **options):
        num_categories = options['num_categories'][0]
        category_names = requests.get(f'http://names.drycodes.com/{num_categories}?nameOptions=objects').json()
        for category_name in category_names:
            description = requests.get(f'https://baconipsum.com/api/?type=meat-and-filler&sentences={random.randrange(1, 4)}&format=text').text

            new_category = Category(name=category_name, description=description)
            new_category.save()

        self.stdout.write(f'Successfully added {num_categories} categories')
