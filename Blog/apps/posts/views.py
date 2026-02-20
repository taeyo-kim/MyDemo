from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.

class PostListView(ListView):
    """블로그 글 목록 뷰"""
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', 'date')
        
        # 정렬 기능
        if sort == 'views':
            queryset = queryset.order_by('-views', '-created_at')
        else:  # sort == 'date' 또는 기본값
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'date')
        return context


class PostDetailView(DetailView):
    """블로그 글 상세 뷰"""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self):
        obj = super().get_object()
        # 조회수 증가
        obj.views += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author').all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """블로그 글 작성 뷰"""
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    
    def form_valid(self, form):
        # 작성자를 현재 로그인한 사용자로 설정
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '새 글 작성'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """블로그 글 수정 뷰"""
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    
    def test_func(self):
        # 작성자만 수정 가능
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '글 수정'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """블로그 글 삭제 뷰"""
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post_list')
    
    def test_func(self):
        # 작성자만 삭제 가능
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    """댓글 작성 뷰"""
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('posts:post_detail', kwargs={'pk': self.kwargs['post_pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """댓글 수정 뷰"""
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_form.html'

    def test_func(self) -> bool:
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self) -> str:
        return reverse('posts:post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """댓글 삭제 뷰"""
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'

    def test_func(self) -> bool:
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self) -> str:
        return reverse('posts:post_detail', kwargs={'pk': self.object.post.pk})

