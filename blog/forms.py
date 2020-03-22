from django import forms
from blog.models import Commentary, Article, Category


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'thumbnail', 'categories']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommentaryForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
