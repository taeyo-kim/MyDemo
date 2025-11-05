from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    """사용자 회원가입 폼"""
    email = forms.EmailField(
        required=True,
        label='이메일',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': '사용자명',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '사용자명을 입력하세요'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호를 다시 입력하세요'
        })
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'

    def clean_email(self):
        """이메일 중복 검사"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('이미 사용 중인 이메일입니다.')
        return email

    def clean_username(self):
        """사용자명 유효성 검사"""
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError('사용자명은 최소 3자 이상이어야 합니다.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('이미 사용 중인 사용자명입니다.')
        return username
