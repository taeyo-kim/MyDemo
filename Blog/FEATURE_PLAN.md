# 블로그 공개 범주 기능 구현 계획

## 개요
블로그 게시글에 공개/비공개 설정 기능을 추가합니다.

## 구현 상세

### 1. 데이터 모델 수정 (apps/posts/models.py)

Post 모델에 `visibility` 필드를 추가합니다:

```python
class Post(models.Model):
    # 공개 범주 선택지
    VISIBILITY_CHOICES = [
        ('PUBLIC', '공개'),
        ('PRIVATE', '비공개'),
    ]
    
    # 기존 필드들...
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='PUBLIC',
        verbose_name='공개 범주'
    )
```

### 2. 폼 수정 (apps/posts/forms.py)

PostForm에 visibility 필드를 추가합니다:

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'visibility']
        widgets = {
            # 기존 위젯들...
            'visibility': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'visibility': '공개 범주',
        }
```

### 3. 뷰 로직 수정 (apps/posts/views.py)

필요한 경우 뷰 로직을 수정하여:
- 비공개 게시글은 작성자만 볼 수 있도록 권한 체크
- 목록에서 비공개 게시글 필터링 (자신의 글은 표시)

### 4. 템플릿 수정

- post_list.html: 공개 범주 표시 (선택사항)
- post_detail.html: 공개 범주 표시
- post_form.html: 공개 범주 선택 필드는 자동으로 표시됨

### 5. 데이터베이스 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```

## 테스트 계획

1. 새 글 작성 시 공개 범주 선택 가능 확인
2. 기존 글 수정 시 공개 범주 변경 가능 확인
3. 비공개 글이 다른 사용자에게 보이지 않는지 확인
4. 작성자는 자신의 비공개 글을 볼 수 있는지 확인

## 향후 개선 사항

- 관리자에게는 모든 글이 보이도록 권한 추가
- 친구 공개, 링크 공유 등 추가 공개 범주 옵션 고려
