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
            category='daily'
        )
        self.assertEqual(memo.category, 'daily')
        self.assertEqual(memo.get_category_display(), '일상')
    
    def test_memo_creation_without_category(self):
        """카테고리가 없는 메모 생성 테스트"""
        memo = Memo.objects.create(
            title='테스트 메모',
            content='테스트 내용',
            author=self.user
        )
        self.assertEqual(memo.category, '')


class MemoCategoryFilteringTest(TestCase):
    """메모 카테고리 필터링 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        
        # 테스트용 메모 생성
        Memo.objects.create(title='일상 메모 1', content='내용', author=self.user, category='daily')
        Memo.objects.create(title='일상 메모 2', content='내용', author=self.user, category='daily')
        Memo.objects.create(title='업무 메모', content='내용', author=self.user, category='work')
        Memo.objects.create(title='개인 메모', content='내용', author=self.user, category='personal')
        Memo.objects.create(title='미분류 메모', content='내용', author=self.user, category='')
    
    def test_filter_by_daily_category(self):
        """일상 카테고리 필터링 테스트"""
        response = self.client.get(reverse('memo_list') + '?category=daily')
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 2)
        for memo in memos:
            self.assertEqual(memo.category, 'daily')
    
    def test_filter_by_work_category(self):
        """업무 카테고리 필터링 테스트"""
        response = self.client.get(reverse('memo_list') + '?category=work')
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 1)
        self.assertEqual(memos[0].category, 'work')
    
    def test_filter_by_personal_category(self):
        """개인 카테고리 필터링 테스트"""
        response = self.client.get(reverse('memo_list') + '?category=personal')
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 1)
        self.assertEqual(memos[0].category, 'personal')
    
    def test_filter_uncategorized_memos(self):
        """미분류 메모 필터링 테스트"""
        response = self.client.get(reverse('memo_list') + '?category=none')
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 1)
        self.assertEqual(memos[0].category, '')
    
    def test_filter_all_memos(self):
        """전체 메모 조회 테스트 (필터 없음)"""
        response = self.client.get(reverse('memo_list'))
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 5)
    
    def test_invalid_category_filter(self):
        """잘못된 카테고리 값으로 필터링 시 빈 결과 반환 테스트"""
        response = self.client.get(reverse('memo_list') + '?category=invalid')
        self.assertEqual(response.status_code, 200)
        memos = response.context['memos']
        self.assertEqual(len(memos), 0)
    
    def test_current_category_in_context(self):
        """컨텍스트에 current_category 포함 확인"""
        response = self.client.get(reverse('memo_list') + '?category=daily')
        self.assertEqual(response.context['current_category'], 'daily')
        
        response = self.client.get(reverse('memo_list'))
        self.assertEqual(response.context['current_category'], 'all')

