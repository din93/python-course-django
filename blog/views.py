from django.shortcuts import render, get_object_or_404, get_list_or_404
from blog.models import Commentary, Article, Category
from blog.forms import CommentaryForm, BlogPostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.base import ContextMixin

class ArticleCommentariesContext(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['commentaries'] = Commentary.objects.filter(article=context['article'])
        context['commentary_form'] = CommentaryForm()
        return context

class BlogHomeView(ListView):
    model = Article
    template_name = 'blog/blog-home.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CreateArticleView(CreateView):
    model = Article
    form_class = BlogPostForm
    template_name = 'blog/article-form.html'
    success_url = reverse_lazy('blog:home')

class UpdateArticleView(UpdateView):
    model = Article
    form_class = BlogPostForm
    template_name = 'blog/article-form.html'

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'pk': self.kwargs['pk']})

class DeleteArticleView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:home')
    context_object_name = 'article'

class DetailArticleView(DetailView, ArticleCommentariesContext):
    model = Article
    template_name = 'blog/article-detail.html'
    context_object_name = 'article'

class CreateCommentView(View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        commentary_form = CommentaryForm(request.POST)
        if commentary_form.is_valid() and commentary_form.has_changed():
            new_commentary = Commentary(
                username='Инкогнито',
                text=commentary_form.cleaned_data['text'],
                article=article
            )
            new_commentary.save()

            return HttpResponseRedirect(reverse('blog:detail', kwargs={'pk': article.pk}))
