from django.shortcuts import render, get_object_or_404, get_list_or_404
from blog.models import Commentary, Article, Category
from users.models import CoursesUser
from blog.forms import CommentaryForm, BlogPostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class BlogHomeView(ListView):
    model = Article
    template_name = 'blog/blog-home.html'
    context_object_name = 'articles'
    queryset = Article.objects.select_related('author').filter(is_shown=True)
    paginate_by = 20
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = BlogPostForm
    template_name = 'blog/article-form.html'
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateArticleView(UserPassesTestMixin, UpdateView):
    model = Article
    form_class = BlogPostForm
    template_name = 'blog/article-form.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'pk': self.kwargs['pk']})

class DeleteArticleView(UserPassesTestMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:home')
    context_object_name = 'article'

    def test_func(self):
        return self.request.user == self.get_object().author or self.request.user.is_superuser

class DetailArticleView(DetailView):
    model = Article
    template_name = 'blog/article-detail.html'
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['article_commentaries'] = context['article'].get_shown_commentaries().select_related('author').all()
        context['commentary_form'] = CommentaryForm()
        return context

class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        commentary_form = CommentaryForm(request.POST)
        if commentary_form.is_valid() and commentary_form.has_changed():
            new_commentary = Commentary(
                author=request.user,
                text=commentary_form.cleaned_data['text'],
                article=article
            )
            new_commentary.save()

            return HttpResponseRedirect(reverse('blog:detail', kwargs={'pk': article.pk}))
