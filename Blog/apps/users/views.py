from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class RegisterView(CreateView):
    """회원가입 뷰"""
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
