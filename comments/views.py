from django.shortcuts import render
from django.shortcuts import get_object_or_404
# from django.http import HttpResponse
from django.urls import reverse_lazy
# from django.views.generic import ListView
# from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CommentForm
from .models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the comments index.")

# class CommentIndexView(ListView):
#   model = Comment
#   queryset = Comment.objects.order_by('-updated_at')
#   paginate_by = 2

def paginate_queryset(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def comments_index(request):
    paginate = request.GET.get(key="paginate", default="2")
    comments_list = Comment.objects.all()
    # comments_list = Comment.objects.all().order_by('-created_at')
    page_obj = paginate_queryset(request, comments_list, paginate)
    context = {
        'comments' : page_obj.object_list,
        'page_obj': page_obj,
        'paginate': paginate,
    }
    return render(request, 'comments/index.html', context)

# class ShowCommentView(DetailView):
#   model = Comment

def comments_show(request, comment_id):
    context = {}
    comment = get_object_or_404(Comment, pk=comment_id)
    context['comment'] = comment
    return render(request, 'comments/show.html', context)

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
    def form_valid(self, form):
        self.object = comment = form.save()
        messages.success(self.request, 'コメントを投稿しました')
        return redirect(self.get_success_url())

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
    def form_valid(self, form):
        self.object = comment = form.save()
        messages.success(self.request, 'コメントを更新しました')
        return redirect(self.get_success_url())

class DeleteCommentView(DeleteView):
    model = Comment
    success_url = reverse_lazy('comments:index')

    def delete(self, request, *args, **kwargs):
        self.object = comment = self.get_object()
        comment.delete()
        messages.success(self.request, 'コメントを削除しました')
        return redirect(self.get_success_url())