from django.core.management.base import BaseCommand, CommandError
from mixer.backend.django import mixer
from faker import Faker
from blog.models import Category

class Command(BaseCommand):
    help = 'Adds random filler for categories'

    def add_arguments(self, parser):
        parser.add_argument('num_categories', nargs='+', type=int)

    def handle(self, *args, **options):
        fake = Faker()
        num_categories = options['num_categories'][0]
        for _ in range(num_categories):
            mixer.blend(Category, name=fake.color_name())

        self.stdout.write(f'Successfully added {num_categories} categories')
