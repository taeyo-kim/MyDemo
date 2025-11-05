from django.contrib import admin
from .models import Memo


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    """메모 관리자 설정"""
    list_display = ['title', 'author', 'category', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author', 'category']
    search_fields = ['title', 'content', 'author__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('기본 정보', {
            'fields': ['title', 'content', 'author', 'category']
        }),
        ('시간 정보', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def get_queryset(self, request):
        """쿼리 최적화"""
        qs = super().get_queryset(request)
        return qs.select_related('author')

