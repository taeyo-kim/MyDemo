from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    """블로그 게시글 모델"""
    VISIBILITY_CHOICES = [
        ('public', '공개'),
        ('private', '비공개'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='작성자',
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    views = models.IntegerField(default=0, verbose_name='조회수')
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='public',
        verbose_name='공개 범주'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.pk})

