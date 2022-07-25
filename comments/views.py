from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
# from django.http import HttpResponse
from django.urls import reverse_lazy
# from django.views.generic import ListView
# from django.views.generic import DetailView
# from django.views.generic import CreateView
# from django.views.generic import UpdateView
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

    # 1つ前（自身の直後に更新されたコメント）を取得する
    prev_comment = Comment.objects.filter(updated_at__gt=comment.updated_at).order_by('updated_at')
    # 1つ後（自身の直前に更新されたコメント）を取得する
    next_comment = Comment.objects.filter(updated_at__lt=comment.updated_at).order_by('-updated_at')
    if len(prev_comment) > 0:
        prev_id = prev_comment[0].id
    else:
        prev_id = False
    if len(next_comment) > 0:
        next_id = next_comment[0].id
    else:
        next_id = False
    context['prev_id'] = prev_id
    context['next_id'] = next_id

    return render(request, 'comments/show.html', context)

# class CreateCommentView(CreateView):
#     model = Comment
#     form_class = CommentForm
#     success_url = reverse_lazy('comments:index')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = 'コメントの投稿'
#         context['form_name'] = 'コメントの投稿'
#         context['button_label'] = 'コメントを投稿する'
#         return context
#     def form_valid(self, form):
#         self.object = comment = form.save()
#         messages.success(self.request, 'コメントを投稿しました')
#         return redirect(self.get_success_url())

def comments_create(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.title = form.cleaned_data.get("title")
            comment.body = form.cleaned_data.get("body")
            comment.save()
            messages.success(request, '投稿しました')
            return redirect(reverse('comments:index'))
        else:
            # エラーメッセージをつけて返す
            context = {}
            context['page_title'] = 'コメントの投稿'
            context['form_name'] = 'コメントの投稿'
            context['button_label'] = 'コメントを投稿する'
            context['form'] = form
            return render(request, 'comments/form.html', context)
    else:
        context = {}
        context['form'] = CommentForm(
                            initial={
                                # 'title' : 'title',
                            }
                        )
        context['page_title'] = 'コメントの投稿'
        context['form_name'] = 'コメントの投稿'
        context['button_label'] = 'コメントを投稿する'
        return render(request, 'comments/form.html', context)


# class UpdateCommentView(UpdateView):
#     model = Comment
#     form_class = CommentForm
#     success_url = reverse_lazy('comments:index')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = 'コメントの更新'
#         context['form_name'] = 'コメントの更新'
#         context['button_label'] = 'コメントを更新する'
#         return context
#     def form_valid(self, form):
#         self.object = comment = form.save()
#         messages.success(self.request, 'コメントを更新しました')
#         return redirect(self.get_success_url())

def comments_update(request, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, pk=comment_id)
            comment.title = form.cleaned_data.get("title")
            comment.body = form.cleaned_data.get("body")
            comment.save()
            messages.success(request, '更新しました')
            return redirect(reverse('comments:index'))
        else:
            # エラーメッセージをつけて返す
            context = {}
            context['page_title'] = 'コメントの編集'
            context['form_name'] = 'コメントの編集'
            context['button_label'] = 'コメントを更新する'
            context['form'] = form
            return render(request, 'comments/form.html', context)
    else:
        context = {}
        comment = get_object_or_404(Comment, pk=comment_id)
        context['form'] = CommentForm(
                            initial={
                                'title' : comment.title,
                                'body' : comment.body,
                            }
                        )
        context['page_title'] = 'コメントの編集'
        context['form_name'] = 'コメントの編集'
        context['button_label'] = 'コメントを更新する'
        return render(request, 'comments/form.html', context)

class DeleteCommentView(DeleteView):
    model = Comment
    success_url = reverse_lazy('comments:index')

    def delete(self, request, *args, **kwargs):
        self.object = comment = self.get_object()
        comment.delete()
        messages.success(self.request, 'コメントを削除しました')
        return redirect(self.get_success_url())