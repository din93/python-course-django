from django.db import models

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

class Article(TimeStamp, Hideable):
    title = models.CharField('Название статьи', max_length=50, unique=False)
    thumbnail = models.ImageField('Картинка статьи', upload_to='thumbnails/blog/', blank=True, null=True)
    text = models.TextField('Текст статьи', blank=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

class Commentary(TimeStamp, Hideable):
    username = models.CharField('Пользователь', max_length=50)
    text = models.CharField('Текст комментария', max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f'From "{self.username}": {self.text}'
