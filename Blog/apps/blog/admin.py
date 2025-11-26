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
    list_display = ['post', 'author', 'short_content', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'post__title', 'author__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    def short_content(self, obj: Comment) -> str:
        """댓글 내용을 50자로 제한하여 표시"""
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content

    short_content.short_description = '내용'
