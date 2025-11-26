from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post


class PostModelTest(TestCase):
    """Post 모델 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        # arrange
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )

    def test_visibility_default_value(self):
        """기본 visibility 값이 PUBLIC인지 확인"""
        # arrange / act
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        # assert
        self.assertEqual(post.visibility, Post.Visibility.PUBLIC)

    def test_is_visible_to_public_post(self):
        """공개 글은 모든 사용자에게 표시됨"""
        # arrange
        post = Post.objects.create(
            title='Public Post',
            content='Content',
            author=self.user,
            visibility=Post.Visibility.PUBLIC
        )
        # act / assert
        self.assertTrue(post.is_visible_to(self.user))
        self.assertTrue(post.is_visible_to(self.other_user))

    def test_is_visible_to_private_post_author(self):
        """비공개 글은 작성자에게 표시됨"""
        # arrange
        post = Post.objects.create(
            title='Private Post',
            content='Content',
            author=self.user,
            visibility=Post.Visibility.PRIVATE
        )
        # act / assert
        self.assertTrue(post.is_visible_to(self.user))

    def test_is_visible_to_private_post_other_user(self):
        """비공개 글은 다른 사용자에게 표시되지 않음"""
        # arrange
        post = Post.objects.create(
            title='Private Post',
            content='Content',
            author=self.user,
            visibility=Post.Visibility.PRIVATE
        )
        # act / assert
        self.assertFalse(post.is_visible_to(self.other_user))


class PostListViewTest(TestCase):
    """PostListView 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        # arrange
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.public_post = Post.objects.create(
            title='Public Post',
            content='Public content',
            author=self.user,
            visibility=Post.Visibility.PUBLIC
        )
        self.private_post = Post.objects.create(
            title='Private Post',
            content='Private content',
            author=self.user,
            visibility=Post.Visibility.PRIVATE
        )

    def test_anonymous_user_sees_only_public_posts(self):
        """비로그인 사용자는 공개 글만 볼 수 있음"""
        # act
        response = self.client.get(reverse('blog:list'))
        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Public Post')
        self.assertNotContains(response, 'Private Post')

    def test_author_sees_all_own_posts(self):
        """작성자는 자신의 모든 글을 볼 수 있음"""
        # arrange
        self.client.login(username='testuser', password='testpass123')
        # act
        response = self.client.get(reverse('blog:list'))
        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Public Post')
        self.assertContains(response, 'Private Post')

    def test_other_user_sees_only_public_posts(self):
        """다른 사용자는 공개 글만 볼 수 있음"""
        # arrange
        self.client.login(username='otheruser', password='testpass123')
        # act
        response = self.client.get(reverse('blog:list'))
        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Public Post')
        self.assertNotContains(response, 'Private Post')


class PostDetailViewTest(TestCase):
    """PostDetailView 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        # arrange
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.public_post = Post.objects.create(
            title='Public Post',
            content='Public content',
            author=self.user,
            visibility=Post.Visibility.PUBLIC
        )
        self.private_post = Post.objects.create(
            title='Private Post',
            content='Private content',
            author=self.user,
            visibility=Post.Visibility.PRIVATE
        )

    def test_public_post_accessible_to_all(self):
        """공개 글은 모든 사용자가 접근 가능"""
        # act
        response = self.client.get(
            reverse('blog:detail', kwargs={'pk': self.public_post.pk})
        )
        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Public Post')

    def test_private_post_accessible_to_author(self):
        """비공개 글은 작성자가 접근 가능"""
        # arrange
        self.client.login(username='testuser', password='testpass123')
        # act
        response = self.client.get(
            reverse('blog:detail', kwargs={'pk': self.private_post.pk})
        )
        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Private Post')

    def test_private_post_not_accessible_to_other_user(self):
        """비공개 글은 다른 사용자가 접근 불가"""
        # arrange
        self.client.login(username='otheruser', password='testpass123')
        # act
        response = self.client.get(
            reverse('blog:detail', kwargs={'pk': self.private_post.pk})
        )
        # assert
        self.assertEqual(response.status_code, 404)

    def test_private_post_not_accessible_to_anonymous(self):
        """비공개 글은 비로그인 사용자가 접근 불가"""
        # act
        response = self.client.get(
            reverse('blog:detail', kwargs={'pk': self.private_post.pk})
        )
        # assert
        self.assertEqual(response.status_code, 404)


class PostCreateViewTest(TestCase):
    """PostCreateView 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        # arrange
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_public_post(self):
        """공개 글 생성"""
        # arrange
        self.client.login(username='testuser', password='testpass123')
        # act
        response = self.client.post(
            reverse('blog:create'),
            {
                'title': 'New Public Post',
                'content': 'New content',
                'visibility': 'PUBLIC'
            }
        )
        # assert
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.visibility, Post.Visibility.PUBLIC)

    def test_create_private_post(self):
        """비공개 글 생성"""
        # arrange
        self.client.login(username='testuser', password='testpass123')
        # act
        response = self.client.post(
            reverse('blog:create'),
            {
                'title': 'New Private Post',
                'content': 'New content',
                'visibility': 'PRIVATE'
            }
        )
        # assert
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.visibility, Post.Visibility.PRIVATE)


class PostUpdateViewTest(TestCase):
    """PostUpdateView 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        # arrange
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.public_post = Post.objects.create(
            title='Public Post',
            content='Public content',
            author=self.user,
            visibility=Post.Visibility.PUBLIC
        )

    def test_update_visibility_to_private(self):
        """공개 글을 비공개로 변경"""
        # arrange
        self.client.login(username='testuser', password='testpass123')
        # act
        response = self.client.post(
            reverse('blog:update', kwargs={'pk': self.public_post.pk}),
            {
                'title': 'Updated Post',
                'content': 'Updated content',
                'visibility': 'PRIVATE'
            }
        )
        # assert
        self.public_post.refresh_from_db()
        self.assertEqual(self.public_post.visibility, Post.Visibility.PRIVATE)
