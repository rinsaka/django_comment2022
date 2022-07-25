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
    def clean(self):
        data = super().clean()
        title = data.get('title')
        body = data.get('body')
        if title is None:
            msg = "タイトルが入力されていません"
            self.add_error('title', msg)
        elif len(title) > 10:
            msg = "タイトルの最大文字数は10文字です"
            self.add_error('title', msg)
        if body is None:
            msg = "本文が入力されていません"
            self.add_error('body', msg)
        elif len(body) > 20:
            msg = "本文の最大文字数は20文字です"
            self.add_error('body', msg)