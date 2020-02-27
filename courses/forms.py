from django import forms
from courses.models import HomeWorkRespond

class HomeWorkRespondForm(forms.ModelForm):
    class Meta:
        model = HomeWorkRespond
        fields = ['text', 'file_attachment']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }