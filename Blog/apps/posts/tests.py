from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment


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


class CommentModelTest(TestCase):
    """Comment 모델 테스트"""

    def setUp(self):
        # arrange
        self.user = User.objects.create_user(username='commenter', password='pass123')
        self.post = Post.objects.create(title='글', content='내용', author=self.user)
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='테스트 댓글입니다.'
        )

    def test_comment_creation(self):
        """댓글 생성 테스트"""
        # assert
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.content, '테스트 댓글입니다.')

    def test_comment_str(self):
        """__str__ 메서드 테스트"""
        # assert
        self.assertIn('commenter', str(self.comment))

    def test_comment_related_name(self):
        """related_name 'comments' 동작 테스트"""
        # assert
        self.assertEqual(self.post.comments.count(), 1)


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

    def test_post_detail_contains_comment_form(self):
        """상세 페이지에 댓글 폼 포함 여부 테스트 (로그인)"""
        # arrange
        self.client.login(username='testuser', password='testpass123')
        # act
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'pk': self.post.pk})
        )
        # assert
        self.assertIn('comment_form', response.context)
        self.assertIn('comments', response.context)


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
                'content': '새 글 내용'
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
                'content': '수정된 내용'
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


class CommentCreateViewTest(TestCase):
    """CommentCreateView 테스트"""

    def setUp(self):
        # arrange
        self.client = Client()
        self.author = User.objects.create_user(username='author', password='pass123')
        self.other = User.objects.create_user(username='other', password='pass123')
        self.post = Post.objects.create(title='글', content='내용', author=self.author)

    def test_comment_create_requires_login(self):
        """비로그인 사용자의 댓글 작성 시도 테스트"""
        # act
        response = self.client.post(
            reverse('posts:comment_create', kwargs={'post_pk': self.post.pk}),
            {'content': '댓글 내용'}
        )
        # assert
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)

    def test_comment_create_with_login(self):
        """로그인한 사용자의 댓글 작성 테스트"""
        # arrange
        self.client.login(username='other', password='pass123')
        # act
        response = self.client.post(
            reverse('posts:comment_create', kwargs={'post_pk': self.post.pk}),
            {'content': '새 댓글입니다.'}
        )
        # assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, '새 댓글입니다.')
        self.assertEqual(comment.author, self.other)
        self.assertEqual(comment.post, self.post)


class CommentUpdateViewTest(TestCase):
    """CommentUpdateView 테스트"""

    def setUp(self):
        # arrange
        self.client = Client()
        self.author = User.objects.create_user(username='author', password='pass123')
        self.other = User.objects.create_user(username='other', password='pass123')
        self.post = Post.objects.create(title='글', content='내용', author=self.author)
        self.comment = Comment.objects.create(
            post=self.post, author=self.author, content='원본 댓글'
        )

    def test_comment_update_by_author(self):
        """작성자의 댓글 수정 테스트"""
        # arrange
        self.client.login(username='author', password='pass123')
        # act
        response = self.client.post(
            reverse('posts:comment_update', kwargs={'pk': self.comment.pk}),
            {'content': '수정된 댓글'}
        )
        # assert
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, '수정된 댓글')

    def test_comment_update_by_non_author(self):
        """작성자가 아닌 사용자의 댓글 수정 시도 테스트"""
        # arrange
        self.client.login(username='other', password='pass123')
        # act
        response = self.client.get(
            reverse('posts:comment_update', kwargs={'pk': self.comment.pk})
        )
        # assert
        self.assertEqual(response.status_code, 403)


class CommentDeleteViewTest(TestCase):
    """CommentDeleteView 테스트"""

    def setUp(self):
        # arrange
        self.client = Client()
        self.author = User.objects.create_user(username='author', password='pass123')
        self.other = User.objects.create_user(username='other', password='pass123')
        self.post = Post.objects.create(title='글', content='내용', author=self.author)
        self.comment = Comment.objects.create(
            post=self.post, author=self.author, content='삭제할 댓글'
        )

    def test_comment_delete_by_author(self):
        """작성자의 댓글 삭제 테스트"""
        # arrange
        self.client.login(username='author', password='pass123')
        # act
        response = self.client.post(
            reverse('posts:comment_delete', kwargs={'pk': self.comment.pk})
        )
        # assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_delete_by_non_author(self):
        """작성자가 아닌 사용자의 댓글 삭제 시도 테스트"""
        # arrange
        self.client.login(username='other', password='pass123')
        # act
        response = self.client.post(
            reverse('posts:comment_delete', kwargs={'pk': self.comment.pk})
        )
        # assert
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.count(), 1)


