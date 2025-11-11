from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """포스트 작성/수정 폼"""
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '포스트 제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '포스트 내용을 입력하세요',
                'rows': 10
            }),
        }
        labels = {
            'title': '제목',
            'content': '내용',
        }
