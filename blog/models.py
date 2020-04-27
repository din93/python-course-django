from django.db import models
from users.models import CoursesUser
from django.utils.functional import cached_property

class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Hideable(models.Model):
    is_shown = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Category(TimeStamp):
    name = models.CharField('Категория', max_length=25, unique=True, null=False)
    description = models.CharField('Описание категории', max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Article(TimeStamp, Hideable):
    title = models.CharField('Название статьи', max_length=50, unique=False)
    thumbnail = models.ImageField('Картинка статьи', upload_to='thumbnails/blog/', blank=True, null=True)
    text = models.TextField('Текст статьи', blank=True)
    categories = models.ManyToManyField(Category, related_name='category_articles')
    author = models.ForeignKey(CoursesUser, on_delete=models.CASCADE)

    def get_shown_commentaries(self):
        return Commentary.objects.filter(article=self, is_shown=True).all()

    @cached_property
    def get_thumbnail_url(self):
        return self.thumbnail if 'http' in self.thumbnail.url else self.thumbnail.url

    @cached_property
    def has_thumbnail(self):
        return bool(self.thumbnail)

    def __str__(self):
        return self.title
    
    @cached_property
    def display_categories(self):
        categories = self.categories.all()
        return ', '.join([category.name for category in categories])

class Commentary(TimeStamp, Hideable):
    author = models.ForeignKey(CoursesUser, on_delete=models.CASCADE, related_name='user_commentaries')
    text = models.CharField('Текст комментария', max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_commentaries')

    def __str__(self):
        return f'From "{self.author.username}": {self.text}'

    class Meta:
        verbose_name_plural = 'Commentaries'
