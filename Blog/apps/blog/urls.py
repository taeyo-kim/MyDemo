from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('new/', views.PostCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    # 댓글 URL
    path('<int:post_pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
