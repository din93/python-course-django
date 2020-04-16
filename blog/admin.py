from django.contrib import admin
from blog.models import Article, Commentary, Category

def show(modeladmin, request, queryset):
    queryset.update(is_shown=True)
show.short_description = "Отображать на сайте"

def hide(modeladmin, request, queryset):
    queryset.update(is_shown=False)
hide.short_description = "Скрыть на сайте"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'has_thumbnail', 'display_categories', 'is_shown']
    actions = [show, hide]

class CommentaryAdmin(admin.ModelAdmin):
    list_display = ['author', 'text', 'article', 'is_shown']
    actions = [show, hide]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Commentary, CommentaryAdmin)
admin.site.register(Category)
