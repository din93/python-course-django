from django.contrib import admin
from courses import models

admin.site.register(models.Course)
admin.site.register(models.CourseChapter)
admin.site.register(models.Lesson)
admin.site.register(models.QuizQuestion)
admin.site.register(models.QuizOption)
admin.site.register(models.Homework)
admin.site.register(models.HomeWorkRespond)
