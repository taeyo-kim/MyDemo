from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """블로그 게시글 모델"""
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

    class Meta:
        ordering = ['-created_at']
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('blog:detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """블로그 댓글 모델"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='게시글',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='작성자',
        related_name='comments'
    )
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        ordering = ['created_at']
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'

    def __str__(self) -> str:
        return f'{self.author.username}의 댓글: {self.content[:20]}'

    def get_absolute_url(self) -> str:
        return reverse('blog:detail', kwargs={'pk': self.post.pk})
