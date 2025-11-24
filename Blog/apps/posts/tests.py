from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post


class PostVisibilityTestCase(TestCase):
    """포스트 공개/비공개 범주 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        # 사용자 생성
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        # 포스트 생성
        self.public_post = Post.objects.create(
            title='공개 포스트',
            content='공개 포스트 내용',
            author=self.user1,
            visibility='public'
        )
        
        self.private_post = Post.objects.create(
            title='비공개 포스트',
            content='비공개 포스트 내용',
            author=self.user1,
            visibility='private'
        )
    
    def test_public_post_visible_to_anonymous(self):
        """공개 포스트는 비로그인 사용자가 볼 수 있음"""
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.public_post.title)
        self.assertNotContains(response, self.private_post.title)
    
    def test_private_post_not_visible_to_anonymous(self):
        """비공개 포스트는 비로그인 사용자가 볼 수 없음"""
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.private_post.pk}))
        # 404 에러가 발생해야 함 (queryset에서 필터링됨)
        self.assertEqual(response.status_code, 404)
    
    def test_private_post_visible_to_author(self):
        """비공개 포스트는 작성자가 볼 수 있음"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.private_post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.private_post.title)
    
    def test_private_post_not_visible_to_other_user(self):
        """비공개 포스트는 다른 사용자가 볼 수 없음"""
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.private_post.pk}))
        # 404 에러가 발생해야 함
        self.assertEqual(response.status_code, 404)
    
    def test_author_sees_own_private_post_in_list(self):
        """작성자는 목록에서 자신의 비공개 포스트를 볼 수 있음"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.public_post.title)
        self.assertContains(response, self.private_post.title)
    
    def test_other_user_does_not_see_private_post_in_list(self):
        """다른 사용자는 목록에서 비공개 포스트를 볼 수 없음"""
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.public_post.title)
        self.assertNotContains(response, self.private_post.title)
    
    def test_create_post_with_visibility(self):
        """포스트 작성 시 공개 범주를 설정할 수 있음"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(reverse('post-create'), {
            'title': '새 포스트',
            'content': '새 포스트 내용',
            'visibility': 'private'
        })
        self.assertEqual(response.status_code, 302)  # 리다이렉트
        new_post = Post.objects.get(title='새 포스트')
        self.assertEqual(new_post.visibility, 'private')
    
    def test_update_post_visibility(self):
        """포스트 수정 시 공개 범주를 변경할 수 있음"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(
            reverse('post-update', kwargs={'pk': self.public_post.pk}),
            {
                'title': self.public_post.title,
                'content': self.public_post.content,
                'visibility': 'private'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.public_post.refresh_from_db()
        self.assertEqual(self.public_post.visibility, 'private')

