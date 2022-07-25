from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    path('', views.comments_index, name='index'),
    path('<int:comment_id>', views.comments_show, name='show'),
    path('create/', views.CreateCommentView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateCommentView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete'),
]