from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import Q
from .models import Post


class PostListView(ListView):
    """블로그 글 목록 뷰"""
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """
        공개 글과 본인의 비공개 글만 반환합니다.
        """
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # 공개 글 또는 본인이 작성한 비공개 글만 표시
            return queryset.filter(
                Q(visibility=Post.Visibility.PUBLIC) |
                Q(author=self.request.user)
            )
        # 비로그인 사용자에게는 공개 글만 표시
        return queryset.filter(visibility=Post.Visibility.PUBLIC)


class PostDetailView(DetailView):
    """블로그 글 상세 뷰"""
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """
        비공개 글에 대한 접근 권한을 확인합니다.
        """
        obj = super().get_object(queryset)
        if not obj.is_visible_to(self.request.user):
            raise Http404("이 게시글에 접근할 수 없습니다.")
        return obj


class PostCreateView(LoginRequiredMixin, CreateView):
    """블로그 글 작성 뷰 (로그인 필수)"""
    model = Post
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'visibility']
    
    def form_valid(self, form):
        # 현재 로그인한 사용자를 작성자로 설정
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """블로그 글 수정 뷰 (로그인 + 작성자 확인)"""
    model = Post
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'visibility']
    
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
