from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Memo(models.Model):
    """메모 모델"""
    title = models.CharField(
        max_length=200,
        verbose_name='제목',
        help_text='메모 제목을 입력하세요'
    )
    content = models.TextField(
        verbose_name='내용',
        help_text='메모 내용을 입력하세요'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='memos',
        verbose_name='작성자'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일시'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일시'
    )

    class Meta:
        verbose_name = '메모'
        verbose_name_plural = '메모 목록'
        ordering = ['-created_at']  # 최신순 정렬
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return f'{self.title} - {self.author.username}'

    def get_absolute_url(self):
        return reverse('memo_detail', kwargs={'pk': self.pk})

    @property
    def is_recently_created(self):
        """최근 24시간 이내 작성 여부"""
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() - self.created_at < timedelta(days=1)

