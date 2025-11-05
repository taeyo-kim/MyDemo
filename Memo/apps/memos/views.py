from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import Memo
from .forms import MemoForm


class MemoListView(LoginRequiredMixin, ListView):
    """메모 목록 뷰"""
    model = Memo
    template_name = 'memos/memo_list.html'
    context_object_name = 'memos'
    paginate_by = 10

    def get_queryset(self):
        """현재 사용자의 메모만 조회 + 범주 필터링"""
        queryset = Memo.objects.filter(author=self.request.user).select_related('author')
        
        # 범주 필터링
        category = self.request.GET.get('category')
        if category:
            if category == 'none':  # 미분류
                queryset = queryset.filter(category__isnull=True)
            elif category in ['daily', 'work', 'personal']:
                queryset = queryset.filter(category=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.request.GET.get('category', 'all')
        return context


class MemoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """메모 상세 뷰"""
    model = Memo
    template_name = 'memos/memo_detail.html'
    context_object_name = 'memo'

    def test_func(self):
        """작성자만 접근 가능"""
        memo = self.get_object()
        return self.request.user == memo.author


class MemoCreateView(LoginRequiredMixin, CreateView):
    """메모 작성 뷰"""
    model = Memo
    form_class = MemoForm
    template_name = 'memos/memo_form.html'

    def form_valid(self, form):
        """작성자 자동 설정"""
        form.instance.author = self.request.user
        messages.success(self.request, '메모가 성공적으로 작성되었습니다!')
        return super().form_valid(form)


class MemoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """메모 수정 뷰"""
    model = Memo
    form_class = MemoForm
    template_name = 'memos/memo_form.html'

    def test_func(self):
        """작성자만 수정 가능"""
        memo = self.get_object()
        return self.request.user == memo.author

    def form_valid(self, form):
        messages.success(self.request, '메모가 성공적으로 수정되었습니다!')
        return super().form_valid(form)


class MemoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """메모 삭제 뷰"""
    model = Memo
    template_name = 'memos/memo_confirm_delete.html'
    success_url = reverse_lazy('memo_list')

    def test_func(self):
        """작성자만 삭제 가능"""
        memo = self.get_object()
        return self.request.user == memo.author

    def delete(self, request, *args, **kwargs):
        messages.success(request, '메모가 성공적으로 삭제되었습니다!')
        return super().delete(request, *args, **kwargs)

