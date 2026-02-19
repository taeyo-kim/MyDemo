from django.contrib import admin
from .models import Post

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

