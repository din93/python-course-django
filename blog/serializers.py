from rest_framework import serializers
from blog.models import Article, Commentary, Category
from users.serializers import CoursesUserSerializer

class CommentarySerializer(serializers.HyperlinkedModelSerializer):
    author = CoursesUserSerializer(read_only=True)
    class Meta:
        model = Commentary
        exclude = ['is_shown']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        exclude = ['created', 'updated']

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    article_commentaries = CommentarySerializer(read_only=True, many=True)
    # categories = CategorySerializer(read_only=True, many=True)
    categories = serializers.StringRelatedField(read_only=True, many=True)
    class Meta:
        model = Article
        exclude = ['is_shown']
