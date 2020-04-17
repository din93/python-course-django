from django.contrib import admin
from courses import models

def show(modeladmin, request, queryset):
    queryset.update(is_shown=True)
show.short_description = "Отображать на сайте"

def hide(modeladmin, request, queryset):
    queryset.update(is_shown=False)
hide.short_description = "Скрыть на сайте"

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'has_thumbnail', 'display_teachers', 'is_shown']
    actions = [show, hide]

admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.CourseChapter)
admin.site.register(models.Lesson)
admin.site.register(models.QuizQuestion)
admin.site.register(models.QuizOption)
admin.site.register(models.Homework)
admin.site.register(models.HomeWorkRespond)
