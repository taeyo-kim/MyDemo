from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post


class PostListView(ListView):
    """블로그 글 목록 뷰"""
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(DetailView):
    """블로그 글 상세 뷰"""
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """블로그 글 작성 뷰 (로그인 필수)"""
    model = Post
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        # 현재 로그인한 사용자를 작성자로 설정
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """블로그 글 수정 뷰 (로그인 + 작성자 확인)"""
    model = Post
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']
    
    def test_func(self):
        # 현재 사용자가 작성자인지 확인
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """블로그 글 삭제 뷰 (로그인 + 작성자 확인)"""
    model = Post
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
    
    def test_func(self):
        # 현재 사용자가 작성자인지 확인
        post = self.get_object()
        return self.request.user == post.author
