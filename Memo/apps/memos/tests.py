from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Memo


class MemoModelTest(TestCase):
    """메모 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_memo_creation_with_category(self):
        """카테고리가 있는 메모 생성 테스트"""
        memo = Memo.objects.create(
            title='테스트 메모',
            content='테스트 내용',
            author=self.user,
            category='private'
        )
        self.assertEqual(memo.category, 'private')
        self.assertEqual(memo.get_category_display(), '개인')
    
    def test_memo_creation_without_category(self):
        """카테고리가 없는 메모 생성 테스트"""
        memo = Memo.objects.create(
            title='테스트 메모',
            content='테스트 내용',
            author=self.user
        )
        self.assertIsNone(memo.category)


class MemoCategoryFilteringTest(TestCase):
    """메모 카테고리 필터링 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        
        # 테스트용 메모 생성
        Memo.objects.create(title='개인 메모 1', content='내용', author=self.user, category='private')
        Memo.objects.create(title='개인 메모 2', content='내용', author=self.user, category='private')
        Memo.objects.create(title='공개 메모', content='내용', author=self.user, category='public')
        Memo.objects.create(title='미분류 메모', content='내용', author=self.user, category=None)
    
    def test_filter_by_private_category(self):
        """개인 카테고리 필터링 테스트"""
        response = self.client.get(reverse('memo_list') + '?category=private')
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 2)
        for memo in memos:
            self.assertEqual(memo.category, 'private')
    
    def test_filter_by_public_category(self):
        """공개 카테고리 필터링 테스트"""
        response = self.client.get(reverse('memo_list') + '?category=public')
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 1)
        self.assertEqual(memos[0].category, 'public')
    
    def test_filter_uncategorized_memos(self):
        """미분류 메모 필터링 테스트"""
        response = self.client.get(reverse('memo_list') + '?category=none')
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 1)
        self.assertIsNone(memos[0].category)
    
    def test_filter_all_memos(self):
        """전체 메모 조회 테스트 (필터 없음)"""
        response = self.client.get(reverse('memo_list'))
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 4)
    
    def test_invalid_category_filter(self):
        """잘못된 카테고리 값으로 필터링 시 전체 메모 반환 테스트"""
        response = self.client.get(reverse('memo_list') + '?category=invalid')
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        # 잘못된 카테고리 값은 무시하고 전체 메모 반환
        self.assertEqual(len(memos), 4)
    
    def test_current_category_in_context(self):
        """컨텍스트에 current_category 포함 확인"""
        response = self.client.get(reverse('memo_list') + '?category=private')
        self.assertEqual(response.context['current_category'], 'private')
        
        response = self.client.get(reverse('memo_list'))
        self.assertEqual(response.context['current_category'], 'all')


