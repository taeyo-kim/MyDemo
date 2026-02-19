from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Post
from .forms import PostForm

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

