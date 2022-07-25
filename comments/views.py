# from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Comment

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the comments index.")

class CommentIndexView(ListView):
  model = Comment

class ShowCommentView(DetailView):
  model = Comment