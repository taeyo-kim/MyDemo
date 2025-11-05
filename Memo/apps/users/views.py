from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    """회원가입 뷰"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}님, 회원가입이 완료되었습니다!')
            login(request, user)
            return redirect('memo_list')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})
