from django.shortcuts import render, get_object_or_404, get_list_or_404
from blog.models import Commentary, Article, Category
from blog.forms import CommentaryForm, BlogPostForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def blog_home(request):
    articles = get_list_or_404(Article)
    categories = Category.objects.all()

    return render(
        request,
        'blog/blog-home.html',
        context={
            'articles': articles,
            'categories': categories
        }
    )

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_article = Article(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                thumbnail=form.cleaned_data['thumbnail']
            )
            new_article.save()
            new_article.categories.add(*form.cleaned_data['categories'])
            new_article.save()

            return HttpResponseRedirect(reverse('blog:home'))
    else:
        form = BlogPostForm()
    return render(
        request,
        'blog/create-blog-post.html',
        context={'form': form}
    )

def blog_detail(request, id):
    article = get_object_or_404(Article, id=id)
    categories = Category.objects.filter(article=article)

    if request.method == 'POST':
        commentary_form = CommentaryForm(request.POST)
        if commentary_form.is_valid() and commentary_form.has_changed():
            new_commentary = Commentary(
                username='Инкогнито',
                text=commentary_form.cleaned_data['text'],
                article=article
            )
            new_commentary.save()
            return HttpResponseRedirect(reverse('blog:detail', kwargs={'id': article.id}))
    commentary_form = CommentaryForm()
    commentaries = Commentary.objects.filter(article=article)

    return render(
        request,
        'blog/blog-post.html',
        context={
            'article': article,
            'commentaries': commentaries,
            'categories': categories,
            'commentary_form': commentary_form
        }
    )
