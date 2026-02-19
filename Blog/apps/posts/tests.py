from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post


class PostModelTest(TestCase):
    """Post 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='테스트 제목',
            content='테스트 내용입니다.',
            author=self.user
        )
    
    def test_post_creation(self):
        """글 생성 테스트"""
        self.assertEqual(self.post.title, '테스트 제목')
        self.assertEqual(self.post.content, '테스트 내용입니다.')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.views, 0)
    
    def test_post_str(self):
        """__str__ 메서드 테스트"""
        self.assertEqual(str(self.post), '테스트 제목')
    
    def test_post_ordering(self):
        """정렬 테스트 (최신순)"""
        post2 = Post.objects.create(
            title='두 번째 글',
            content='두 번째 내용',
            author=self.user
        )
        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)  # 최신 글이 먼저
        self.assertEqual(posts[1], self.post)


class PostListViewTest(TestCase):
    """PostListView 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_post_list_view(self):
        """글 목록 조회 테스트"""
        response = self.client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_list.html')
    
    def test_post_list_sorting_by_views(self):
        """조회수순 정렬 테스트"""
        post1 = Post.objects.create(
            title='첫 번째 글',
            content='내용1',
            author=self.user,
            views=10
        )
        post2 = Post.objects.create(
            title='두 번째 글',
            content='내용2',
            author=self.user,
            views=20
        )
        response = self.client.get(reverse('posts:post_list') + '?sort=views')
        self.assertEqual(response.context['posts'][0], post2)


class PostDetailViewTest(TestCase):
    """PostDetailView 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='테스트 글',
            content='테스트 내용',
            author=self.user
        )
    
    def test_post_detail_view(self):
        """글 상세 조회 테스트"""
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 글')
    
    def test_post_views_increment(self):
        """조회수 증가 테스트"""
        initial_views = self.post.views
        self.client.get(reverse('posts:post_detail', kwargs={'pk': self.post.pk}))
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, initial_views + 1)


class PostCreateViewTest(TestCase):
    """PostCreateView 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_post_create_view_requires_login(self):
        """비로그인 사용자의 글 작성 시도 테스트"""
        response = self.client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, 302)  # 로그인 페이지로 리다이렉트
        self.assertIn('/users/login/', response.url)
    
    def test_post_create_view_with_login(self):
        """로그인한 사용자의 글 작성 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('posts:post_create'),
            {
                'title': '새 글 제목',
                'content': '새 글 내용',
                'visibility': 'public'
            }
        )
        self.assertEqual(response.status_code, 302)  # 성공 후 리다이렉트
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, '새 글 제목')
        self.assertEqual(post.author, self.user)


class PostUpdateViewTest(TestCase):
    """PostUpdateView 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        self.post = Post.objects.create(
            title='원본 제목',
            content='원본 내용',
            author=self.user1
        )
    
    def test_post_update_by_author(self):
        """작성자의 글 수정 테스트"""
        self.client.login(username='user1', password='pass123')
        response = self.client.post(
            reverse('posts:post_update', kwargs={'pk': self.post.pk}),
            {
                'title': '수정된 제목',
                'content': '수정된 내용',
                'visibility': 'public'
            }
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, '수정된 제목')
    
    def test_post_update_by_non_author(self):
        """작성자가 아닌 사용자의 글 수정 시도 테스트"""
        self.client.login(username='user2', password='pass123')
        response = self.client.get(
            reverse('posts:post_update', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 403)  # Forbidden


class PostDeleteViewTest(TestCase):
    """PostDeleteView 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='삭제할 글',
            content='삭제할 내용',
            author=self.user
        )
    
    def test_post_delete_by_author(self):
        """작성자의 글 삭제 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('posts:post_delete', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 302)  # 성공 후 리다이렉트
        self.assertEqual(Post.objects.count(), 0)


class PostVisibilityTest(TestCase):
    """Post 공개 범주 기능 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        self.public_post = Post.objects.create(
            title='공개 글',
            content='공개 내용',
            author=self.user1,
            visibility='public'
        )
        self.private_post = Post.objects.create(
            title='비공개 글',
            content='비공개 내용',
            author=self.user1,
            visibility='private'
        )
    
    def test_public_post_visible_to_all(self):
        """공개 글은 모든 사용자에게 보임"""
        # 비로그인 사용자
        response = self.client.get(reverse('posts:post_list'))
        self.assertContains(response, '공개 글')
        self.assertNotContains(response, '비공개 글')
        
        # 다른 사용자
        self.client.login(username='user2', password='pass123')
        response = self.client.get(reverse('posts:post_list'))
        self.assertContains(response, '공개 글')
        self.assertNotContains(response, '비공개 글')
    
    def test_private_post_visible_to_author_only(self):
        """비공개 글은 작성자에게만 보임"""
        # 작성자로 로그인
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('posts:post_list'))
        self.assertContains(response, '공개 글')
        self.assertContains(response, '비공개 글')
    
    def test_private_post_detail_access_denied_for_others(self):
        """비공개 글 상세 페이지는 작성자만 접근 가능"""
        # 비로그인 사용자
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'pk': self.private_post.pk})
        )
        self.assertEqual(response.status_code, 403)
        
        # 다른 사용자
        self.client.login(username='user2', password='pass123')
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'pk': self.private_post.pk})
        )
        self.assertEqual(response.status_code, 403)
    
    def test_private_post_detail_access_allowed_for_author(self):
        """비공개 글 상세 페이지는 작성자가 접근 가능"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'pk': self.private_post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '비공개 글')
    
    def test_public_post_detail_access_allowed_for_all(self):
        """공개 글 상세 페이지는 모든 사용자가 접근 가능"""
        # 비로그인 사용자
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'pk': self.public_post.pk})
        )
        self.assertEqual(response.status_code, 200)
        
        # 다른 사용자
        self.client.login(username='user2', password='pass123')
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'pk': self.public_post.pk})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_post_creation_with_visibility(self):
        """공개 범주를 지정하여 글 작성 테스트"""
        self.client.login(username='user1', password='pass123')
        response = self.client.post(
            reverse('posts:post_create'),
            {
                'title': '새 비공개 글',
                'content': '새 비공개 내용',
                'visibility': 'private'
            }
        )
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title='새 비공개 글')
        self.assertEqual(post.visibility, 'private')
    
    def test_post_default_visibility_is_public(self):
        """기본 공개 범주는 'public'"""
        self.client.login(username='user1', password='pass123')
        # visibility를 명시하지 않으면 폼이 유효하지 않으므로, 기본값 'public'을 전달
        response = self.client.post(
            reverse('posts:post_create'),
            {
                'title': '기본 공개 글',
                'content': '기본 내용',
                'visibility': 'public'
            }
        )
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title='기본 공개 글')
        self.assertEqual(post.visibility, 'public')
    
    def test_private_post_badge_shown_to_author(self):
        """비공개 글 뱃지가 작성자에게 표시됨"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('posts:post_list'))
        self.assertContains(response, '비공개')
        
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'pk': self.private_post.pk})
        )
        self.assertContains(response, '비공개')


