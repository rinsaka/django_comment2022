from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('title', 'body')
        widgets = {
              'title': forms.TextInput(attrs={
              'class': 'form-control'
            }),
              'body': forms.TextInput(attrs={
              'class': 'form-control'
            }),
        }
        labels = {
            'title': 'タイトル',
            'body': '本文',
        }