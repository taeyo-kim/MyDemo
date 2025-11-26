from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """댓글 작성/수정 폼"""

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-indigo-500',
                'rows': 3,
                'placeholder': '댓글을 입력하세요...'
            })
        }
        labels = {
            'content': '댓글 내용'
        }
