from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post


class PostVisibilityTestCase(TestCase):
    """블로그 글 공개/비공개 기능 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        # 테스트 사용자 생성
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        # 공개 글 생성
        self.public_post = Post.objects.create(
            title='공개 글',
            content='이것은 공개 글입니다.',
            author=self.user1,
            visibility='public'
        )
        
        # 비공개 글 생성 (user1 작성)
        self.private_post = Post.objects.create(
            title='비공개 글',
            content='이것은 비공개 글입니다.',
            author=self.user1,
            visibility='private'
        )
    
    def test_public_post_visible_to_all(self):
        """공개 글은 모든 사용자가 조회 가능"""
        # 비로그인 사용자
        response = self.client.get(reverse('blog:detail', args=[self.public_post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '공개 글')
        
        # 로그인 사용자 (user2)
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(reverse('blog:detail', args=[self.public_post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '공개 글')
    
    def test_private_post_not_visible_to_anonymous(self):
        """비공개 글은 비로그인 사용자가 조회 불가"""
        response = self.client.get(reverse('blog:detail', args=[self.private_post.pk]))
        self.assertEqual(response.status_code, 404)
    
    def test_private_post_not_visible_to_other_users(self):
        """비공개 글은 다른 사용자가 조회 불가"""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(reverse('blog:detail', args=[self.private_post.pk]))
        self.assertEqual(response.status_code, 404)
    
    def test_private_post_visible_to_author(self):
        """비공개 글은 작성자만 조회 가능"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('blog:detail', args=[self.private_post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '비공개 글')
    
    def test_list_view_filters_private_posts(self):
        """목록 뷰에서 비공개 글 필터링 확인"""
        # 비로그인 사용자: 공개 글만 보임
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '공개 글')
        self.assertNotContains(response, '비공개 글')
        
        # 다른 사용자: 공개 글만 보임
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '공개 글')
        self.assertNotContains(response, '비공개 글')
        
        # 작성자: 공개 글과 자신의 비공개 글 모두 보임
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '공개 글')
        self.assertContains(response, '비공개 글')
    
    def test_create_post_with_visibility(self):
        """글 작성 시 공개 범주 설정 확인"""
        self.client.login(username='testuser1', password='testpass123')
        
        # 비공개 글 작성
        response = self.client.post(reverse('blog:create'), {
            'title': '새 비공개 글',
            'content': '새로운 비공개 글입니다.',
            'visibility': 'private'
        })
        
        # 성공적으로 생성되었는지 확인
        self.assertEqual(response.status_code, 302)  # 리다이렉트
        
        # 생성된 글 확인
        new_post = Post.objects.get(title='새 비공개 글')
        self.assertEqual(new_post.visibility, 'private')
        self.assertEqual(new_post.author, self.user1)
    
    def test_update_post_visibility(self):
        """글 수정 시 공개 범주 변경 확인"""
        self.client.login(username='testuser1', password='testpass123')
        
        # 공개 글을 비공개로 변경
        response = self.client.post(
            reverse('blog:update', args=[self.public_post.pk]),
            {
                'title': self.public_post.title,
                'content': self.public_post.content,
                'visibility': 'private'
            }
        )
        
        # 성공적으로 수정되었는지 확인
        self.assertEqual(response.status_code, 302)  # 리다이렉트
        
        # 변경된 공개 범주 확인
        self.public_post.refresh_from_db()
        self.assertEqual(self.public_post.visibility, 'private')
    
    def test_default_visibility_is_public(self):
        """기본 공개 범주가 '공개'인지 확인"""
        self.client.login(username='testuser1', password='testpass123')
        
        # visibility를 명시적으로 설정하지 않은 경우 기본값 확인
        # Django 폼에서는 필드가 있으므로 기본값이 선택됨
        response = self.client.post(reverse('blog:create'), {
            'title': '기본 공개 범주 테스트',
            'content': '기본값 테스트 글입니다.',
            'visibility': ''  # 빈 값으로 제출 시 기본값 사용
        })
        
        # 성공적으로 생성되었는지 확인 (기본값으로 처리됨)
        # 또는 직접 모델 생성 시 기본값 테스트
        test_post = Post.objects.create(
            title='모델 기본값 테스트',
            content='모델 직접 생성 테스트',
            author=self.user1
        )
        self.assertEqual(test_post.visibility, 'public')
    
    def test_visibility_badge_display(self):
        """공개/비공개 배지 표시 확인"""
        self.client.login(username='testuser1', password='testpass123')
        
        # 공개 글 상세 페이지
        response = self.client.get(reverse('blog:detail', args=[self.public_post.pk]))
        self.assertContains(response, '공개')
        
        # 비공개 글 상세 페이지
        response = self.client.get(reverse('blog:detail', args=[self.private_post.pk]))
        self.assertContains(response, '비공개')

