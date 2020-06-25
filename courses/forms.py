from django import forms
from courses.models import HomeWorkRespond, Course, CourseChapter, Lesson, Homework, HWRespondCommentary

class HomeWorkRespondForm(forms.ModelForm):
    class Meta:
        model = HomeWorkRespond
        fields = ['text', 'file_attachment']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control bg-light', 'rows': 3}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class CourseChapterForm(forms.ModelForm):
    class Meta:
        model = CourseChapter
        fields = ['title', 'number']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '№'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'number', 'estimated_time_min', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '№'}),
            'estimated_time_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['points', 'text']

        widgets = {
            'points': forms.NumberInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

class HWRespondCommentaryForm(forms.ModelForm):
    class Meta:
        model = HWRespondCommentary
        fields = ['text']

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Добавить комментарий'}),
        }