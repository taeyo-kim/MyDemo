from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """블로그 글 작성/수정 폼"""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'visibility']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': '제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': '내용을 입력하세요',
                'rows': 10
            }),
            'visibility': forms.RadioSelect(attrs={
                'class': 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300'
            }),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'visibility': '공개 범주',
        }
