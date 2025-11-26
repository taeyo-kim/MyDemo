from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post 모델 관리자 페이지 설정"""
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment 모델 관리자 페이지 설정"""
    list_display = ['post', 'author', 'content', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'post__title', 'author__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
