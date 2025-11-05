from django import forms
from .models import Memo


class MemoForm(forms.ModelForm):
    """메모 작성/수정 폼"""
    
    class Meta:
        model = Memo
        fields = ['title', 'content']
        labels = {
            'title': '제목',
            'content': '내용',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '메모 제목을 입력하세요',
                'maxlength': '200',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '메모 내용을 입력하세요',
                'rows': 10,
            }),
        }

    def clean_title(self):
        """제목 유효성 검사"""
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise forms.ValidationError('제목은 최소 2자 이상이어야 합니다.')
        return title

    def clean_content(self):
        """내용 유효성 검사"""
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise forms.ValidationError('내용은 최소 5자 이상이어야 합니다.')
        return content
