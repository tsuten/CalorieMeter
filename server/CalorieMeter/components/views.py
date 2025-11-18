from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.files.storage import default_storage
from django.conf import settings
# from core.models import Meal # 不使用
from users.models import AuthAccount
from users.decorator import login_required_check_user_profile
# from .utils import classify_food_image
# Create your views here.

# メインページ(ログイン・サインアップ前用)へ遷移 usersのviews.indexへ遷移
def main_page():
    return redirect('users:index')


@login_required_check_user_profile
def index(request):
    return render(request, 'index.html')


def calendar(request):
    return render(request, 'calendar.html')

# @login_required
def statistics(request):
    return render(request, 'statistics.html')

def profile(request):
    return render(request, 'profile.html')

def record(request):
    return render(request, 'record.html')

def error(request):
    message = request.GET.get('message', '不明なエラーが発生しました。')
    return render(request, 'error.html', {'message': message}) 