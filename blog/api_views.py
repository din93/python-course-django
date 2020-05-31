from rest_framework import viewsets
from blog.models import Article, Commentary, Category
from blog.serializers import ArticleSerializer, CommentarySerializer, CategorySerializer
from rest_framework import permissions
from blog.permissions import ReadOnly, isAuthorOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

# ViewSets define the view behavior.
class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [isAuthorOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Article.objects.select_related('author').filter(is_shown=True)
    serializer_class = ArticleSerializer

class CommentaryViewSet(viewsets.ModelViewSet):
    permission_classes = [isAuthorOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Commentary.objects.select_related('author').filter(is_shown=True)
    serializer_class = CommentarySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated|ReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer