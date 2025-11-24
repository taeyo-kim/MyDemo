from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    """포스트 목록 뷰"""
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']
    
    def get_queryset(self):
        """비로그인 사용자: 공개 글만, 로그인 사용자: 공개 글 + 본인 비공개 글"""
        queryset = super().get_queryset()
        
        if self.request.user.is_authenticated:
            # 로그인 사용자: 공개 글 또는 본인의 비공개 글
            queryset = queryset.filter(
                Q(visibility='public') | Q(author=self.request.user)
            )
        else:
            # 비로그인 사용자: 공개 글만
            queryset = queryset.filter(visibility='public')
        
        return queryset


class PostDetailView(DetailView):
    """포스트 상세 뷰"""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """비공개 글은 작성자만 접근 가능"""
        queryset = super().get_queryset()
        
        if self.request.user.is_authenticated:
            # 로그인 사용자: 공개 글 또는 본인의 비공개 글
            queryset = queryset.filter(
                Q(visibility='public') | Q(author=self.request.user)
            )
        else:
            # 비로그인 사용자: 공개 글만
            queryset = queryset.filter(visibility='public')
        
        return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    """포스트 작성 뷰"""
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '포스트가 작성되었습니다.')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """포스트 수정 뷰"""
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, '포스트가 수정되었습니다.')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """포스트 삭제 뷰"""
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '포스트가 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)

