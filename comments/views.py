# from django.shortcuts import render
# from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from .forms import CommentForm
from .models import Comment

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the comments index.")

class CommentIndexView(ListView):
  model = Comment

class ShowCommentView(DetailView):
  model = Comment

class CreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('comments:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'コメントの投稿'
        context['form_name'] = 'コメントの投稿'
        context['button_label'] = 'コメントを投稿する'
        return context

class UpdateCommentView(UpdateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('comments:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'コメントの更新'
        context['form_name'] = 'コメントの更新'
        context['button_label'] = 'コメントを更新する'
        return context