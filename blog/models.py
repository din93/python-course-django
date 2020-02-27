from django.db import models

class Category(models.Model):
    name = models.CharField('Категория', max_length=25, unique=True, null=False)
    description = models.CharField('Описание категории', max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField('Название статьи', max_length=50, unique=False)
    thumbnail = models.ImageField('Картинка статьи', upload_to='thumbnails/blog/', blank=True, null=True)
    text = models.TextField('Текст статьи', blank=True)
    categories = models.ManyToManyField(Category)
    created = models.DateTimeField(auto_now_add=True)
    is_shown = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Commentary(models.Model):
    username = models.CharField(max_length=50)
    text = models.CharField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_shown = models.BooleanField(default=True)

    def __str__(self):
        return f'From "{self.username}": {self.text}'
