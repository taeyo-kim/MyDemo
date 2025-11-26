from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import CommentForm


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

    def get_context_data(self, **kwargs) -> dict:
        """댓글 목록과 댓글 작성 폼을 컨텍스트에 추가"""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """블로그 글 작성 뷰 (로그인 필수)"""
    model = Post
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']

    def form_valid(self, form) -> HttpResponse:
        # 현재 로그인한 사용자를 작성자로 설정
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """블로그 글 수정 뷰 (로그인 + 작성자 확인)"""
    model = Post
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']

    def test_func(self) -> bool:
        # 현재 사용자가 작성자인지 확인
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """블로그 글 삭제 뷰 (로그인 + 작성자 확인)"""
    model = Post
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')

    def test_func(self) -> bool:
        # 현재 사용자가 작성자인지 확인
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    """댓글 작성 뷰 (로그인 필수)"""
    model = Comment
    form_class = CommentForm

    def form_valid(self, form) -> HttpResponse:
        # 현재 로그인한 사용자를 작성자로 설정
        form.instance.author = self.request.user
        # URL에서 post_pk를 가져와 게시글 설정
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('blog:detail', kwargs={'pk': self.kwargs['post_pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """댓글 수정 뷰 (로그인 + 작성자 확인)"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self) -> bool:
        # 현재 사용자가 작성자인지 확인
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self) -> str:
        return reverse('blog:detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """댓글 삭제 뷰 (로그인 + 작성자 확인)"""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self) -> bool:
        # 현재 사용자가 작성자인지 확인
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self) -> str:
        return reverse('blog:detail', kwargs={'pk': self.object.post.pk})
