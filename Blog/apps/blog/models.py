from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """블로그 게시글 모델"""
    
    class Visibility(models.TextChoices):
        """게시글 공개 범주 옵션"""
        PUBLIC = 'PUBLIC', '공개'
        PRIVATE = 'PRIVATE', '비공개'
    
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='작성자',
        related_name='posts'
    )
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
        verbose_name='공개 범주'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def is_visible_to(self, user) -> bool:
        """
        특정 사용자에게 게시글이 표시되는지 확인합니다.
        
        Args:
            user: 확인할 사용자 객체
            
        Returns:
            bool: 사용자에게 게시글이 표시되면 True, 아니면 False
        """
        if self.visibility == self.Visibility.PUBLIC:
            return True
        return user.is_authenticated and user == self.author
