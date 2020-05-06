from rest_framework import viewsets
from blog.models import Article, Commentary, Category
from blog.serializers import ArticleSerializer, CommentarySerializer, CategorySerializer

# ViewSets define the view behavior.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author').filter(is_shown=True)
    serializer_class = ArticleSerializer

class CommentaryViewSet(viewsets.ModelViewSet):
    queryset = Commentary.objects.select_related('author').filter(is_shown=True)
    serializer_class = CommentarySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer