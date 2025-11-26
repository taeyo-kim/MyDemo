from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment


class CommentModelTest(TestCase):
    """Comment 모델 테스트"""

    def setUp(self) -> None:
        # arrange
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )

    def test_comment_creation(self) -> None:
        """댓글 생성 테스트"""
        # arrange
        content = '테스트 댓글입니다.'

        # act
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content=content
        )

        # assert
        self.assertEqual(comment.content, content)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

    def test_comment_str_method(self) -> None:
        """댓글 __str__ 메서드 테스트"""
        # arrange
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='테스트 댓글입니다.'
        )

        # act
        result = str(comment)

        # assert
        self.assertIn(self.user.username, result)

    def test_comment_ordering(self) -> None:
        """댓글 정렬 순서 테스트 (작성일 오름차순)"""
        # arrange
        comment1 = Comment.objects.create(
            post=self.post, author=self.user, content='첫 번째 댓글'
        )
        comment2 = Comment.objects.create(
            post=self.post, author=self.user, content='두 번째 댓글'
        )

        # act
        comments = list(self.post.comments.all())

        # assert
        self.assertEqual(comments[0], comment1)
        self.assertEqual(comments[1], comment2)


class CommentViewTest(TestCase):
    """Comment 뷰 테스트"""

    def setUp(self) -> None:
        # arrange
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='테스트 댓글'
        )

    def test_comment_create_view_requires_login(self) -> None:
        """비로그인 사용자는 댓글 작성 불가"""
        # arrange
        url = reverse('blog:comment_create', kwargs={'post_pk': self.post.pk})

        # act
        response = self.client.post(url, {'content': '새 댓글'})

        # assert
        self.assertEqual(response.status_code, 302)  # 로그인 페이지로 리다이렉트
        self.assertIn('login', response.url)

    def test_comment_create_view_authenticated_user(self) -> None:
        """로그인 사용자는 댓글 작성 가능"""
        # arrange
        self.client.login(username='testuser', password='testpass123')
        url = reverse('blog:comment_create', kwargs={'post_pk': self.post.pk})

        # act
        response = self.client.post(url, {'content': '새 댓글'})

        # assert
        self.assertEqual(response.status_code, 302)  # 성공 후 리다이렉트
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_update_view_only_author_can_update(self) -> None:
        """작성자만 댓글 수정 가능"""
        # arrange - 다른 사용자로 로그인
        self.client.login(username='otheruser', password='otherpass123')
        url = reverse('blog:comment_update', kwargs={'pk': self.comment.pk})

        # act
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, 403)  # 권한 없음

    def test_comment_update_view_author_can_update(self) -> None:
        """작성자는 댓글 수정 가능"""
        # arrange
        self.client.login(username='testuser', password='testpass123')
        url = reverse('blog:comment_update', kwargs={'pk': self.comment.pk})

        # act
        response = self.client.post(url, {'content': '수정된 댓글'})

        # assert
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, '수정된 댓글')

    def test_comment_delete_view_only_author_can_delete(self) -> None:
        """작성자만 댓글 삭제 가능"""
        # arrange - 다른 사용자로 로그인
        self.client.login(username='otheruser', password='otherpass123')
        url = reverse('blog:comment_delete', kwargs={'pk': self.comment.pk})

        # act
        response = self.client.post(url)

        # assert
        self.assertEqual(response.status_code, 403)  # 권한 없음
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_comment_delete_view_author_can_delete(self) -> None:
        """작성자는 댓글 삭제 가능"""
        # arrange
        self.client.login(username='testuser', password='testpass123')
        url = reverse('blog:comment_delete', kwargs={'pk': self.comment.pk})

        # act
        response = self.client.post(url)

        # assert
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_post_detail_view_shows_comments(self) -> None:
        """블로그 상세 페이지에 댓글 목록 표시"""
        # arrange
        url = reverse('blog:detail', kwargs={'pk': self.post.pk})

        # act
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 댓글')
        self.assertIn('comments', response.context)
        self.assertIn('comment_form', response.context)

