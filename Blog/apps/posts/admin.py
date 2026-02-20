from django.contrib import admin
from .models import Post, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post 모델 관리자 설정"""
    list_display = ['title', 'author', 'views', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'views']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment 모델 관리자 설정"""
    list_display = ['author', 'post', 'short_content', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    @admin.display(description='내용')
    def short_content(self, obj: Comment) -> str:
        """댓글 내용 앞 50자 반환"""
        return obj.content[:50]

